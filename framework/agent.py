"""Agent framework for autonomous task execution with tool calling.

This module implements an agent that uses the OpenRouter API for LLM inference,
supporting streaming responses, tool calling, and reasoning token display.
"""

import json
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any

from framework.llm import OpenRouterClient, OpenRouterConfig, TokenUsage
from framework.verifier import Verifier

# Prefix that indicates the agent should stop (answer was submitted)
# This avoids global state - the tool result signals completion
ANSWER_SUBMITTED_PREFIX = "ANSWER_SUBMITTED:"

type ToolFunction = Callable[..., str]


class EventType(Enum):
    """Types of events emitted during agent execution."""

    # Generation events
    GENERATION_START = auto()
    THINKING_START = auto()
    THINKING_CHUNK = auto()
    THINKING_END = auto()
    RESPONSE_CHUNK = auto()
    GENERATION_END = auto()

    # Tool events
    TOOL_CALL_START = auto()
    TOOL_CALL_PARSED = auto()
    TOOL_EXECUTION_START = auto()
    TOOL_EXECUTION_END = auto()

    # Agent loop events
    ITERATION_START = auto()
    ITERATION_END = auto()
    AGENT_COMPLETE = auto()
    AGENT_ERROR = auto()


@dataclass
class AgentEvent:
    """An event emitted during agent execution."""

    type: EventType
    data: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        """Format event for display."""
        return f"[{self.type.name}] {self.data}"


@dataclass
class Tool:
    """Represents a tool that can be called by the agent.

    Tool functions must return a string that will be shown to the LLM.
    """

    name: str
    description: str
    parameters: dict[str, Any]
    function: ToolFunction


@dataclass
class ToolCall:
    """Represents a (parsed) tool call request from the agent."""

    id: str  # Required for OpenAI-compatible API
    name: str
    arguments: dict[str, Any]
    error: str | None = None


@dataclass
class Message:
    """Represents a message in the conversation."""

    role: str  # "system", "user", "assistant", or "tool"
    content: str | None = None
    tool_calls: list[dict[str, Any]] | None = None  # For assistant messages with tool calls
    tool_call_id: str | None = None  # For tool result messages


@dataclass
class ContextCompressionSettings:
    """Settings for context compression to reduce token usage."""

    enabled: bool = False
    keep_recent: int = 3  # Number of recent tool results to keep in full
    max_chars: int = 150  # Max chars for truncated older results


@dataclass
class Conversation:
    """Represents a conversation between the agent and the user."""

    messages: list[Message] = field(default_factory=list)

    def to_api_format(
        self,
        compression: ContextCompressionSettings | None = None,
    ) -> list[dict[str, Any]]:
        """Convert the conversation to OpenAI-compatible API format.

        Args:
            compression: Optional compression settings. If enabled, older tool
                results are truncated and duplicate consecutive tool calls are
                deduplicated.
        """
        messages_to_convert = self.messages

        if compression and compression.enabled:
            messages_to_convert = _compress_messages(
                self.messages,
                keep_recent=compression.keep_recent,
                max_chars=compression.max_chars,
            )

        result: list[dict[str, Any]] = []
        for message in messages_to_convert:
            msg: dict[str, Any] = {"role": message.role}

            if message.content is not None:
                msg["content"] = message.content

            if message.tool_calls is not None:
                msg["tool_calls"] = message.tool_calls

            if message.tool_call_id is not None:
                msg["tool_call_id"] = message.tool_call_id

            result.append(msg)
        return result


def _truncate_tool_result(content: str, max_chars: int) -> str:
    """Truncate a tool result to max_chars with a summary prefix."""
    if len(content) <= max_chars:
        return content

    # Extract first line as summary (often contains row/column counts)
    first_line = content.split("\n")[0]
    if len(first_line) <= max_chars - 20:
        return f"[Truncated] {first_line}"

    return f"[Truncated] {content[:max_chars - 15]}..."


def _compress_messages(
    messages: list[Message],
    keep_recent: int,
    max_chars: int,
) -> list[Message]:
    """Compress messages by truncating old tool results and deduplicating.

    Applies two optimizations:
    1. Truncates tool results older than keep_recent to max_chars
    2. Removes duplicate consecutive tool calls with identical results
    """
    # Find all tool message indices (for determining which are "recent")
    tool_indices: list[int] = [
        i for i, m in enumerate(messages) if m.role == "tool"
    ]

    # Indices of tool messages to keep in full (the most recent ones)
    recent_tool_indices = set(tool_indices[-keep_recent:]) if tool_indices else set()

    # Build compressed message list
    result: list[Message] = []
    seen_tool_calls: dict[str, str] = {}  # (name, args_json) -> full result

    for i, msg in enumerate(messages):
        if msg.role == "tool":
            # Check for deduplication: same tool call with same result
            # Find the corresponding assistant message's tool call
            tool_key: str | None = None
            for j in range(i - 1, -1, -1):
                assistant_tool_calls = messages[j].tool_calls
                if messages[j].role == "assistant" and assistant_tool_calls:
                    for tc in assistant_tool_calls:
                        if tc.get("id") == msg.tool_call_id:
                            name = tc.get("function", {}).get("name", "")
                            args = tc.get("function", {}).get("arguments", "")
                            tool_key = f"{name}:{args}"
                            break
                    break

            # Deduplicate: if we've seen this exact call before with same result
            if tool_key and msg.content:
                if tool_key in seen_tool_calls:
                    prev_content = seen_tool_calls[tool_key]
                    if prev_content == msg.content:
                        # Skip this duplicate - but we need to keep the message
                        # structure for the API, so mark it as deduplicated
                        result.append(
                            Message(
                                role=msg.role,
                                content="[Duplicate call - see earlier result]",
                                tool_call_id=msg.tool_call_id,
                            )
                        )
                        continue
                seen_tool_calls[tool_key] = msg.content

            # Truncate if not in recent set
            if i not in recent_tool_indices and msg.content:
                result.append(
                    Message(
                        role=msg.role,
                        content=_truncate_tool_result(msg.content, max_chars),
                        tool_call_id=msg.tool_call_id,
                    )
                )
            else:
                result.append(msg)
        else:
            result.append(msg)

    return result


class Agent:
    """Implements a tiny, generic agent framework.

    Built on top of the OpenRouter API client.

    Only supports a single model, streaming, and an extensible tool set.
    """

    # Pre-submission verifier model (used by all Agent instances)
    VERIFIER_MODEL = "moonshotai/kimi-k2.5"
    # Guide-retrieval validator model
    GUIDE_VALIDATOR_MODEL = "openai/gpt-oss-120b:nitro"
    # Max times the verifier can reject before we let submit_answer through
    MAX_VERIFY_REJECTIONS = 1

    def __init__(self, config: OpenRouterConfig, tools: dict[str, Tool]):
        self.config = config
        self.tools: dict[str, Tool] = tools  # mapping from tool name to tool object
        self.client: OpenRouterClient = OpenRouterClient(config)
        self.conversation: Conversation = Conversation()
        self._compression = ContextCompressionSettings(
            enabled=config.compress_context,
            keep_recent=config.compress_keep_recent,
            max_chars=config.compress_max_chars,
        )

        # Pre-submission SQL verifier (secondary LLM)
        self._verifier = Verifier(
            api_key=config.api_key,
            model=self.VERIFIER_MODEL,
        )
        self._verify_rejections = 0
        self._original_prompt = ""

        # Initialise the business-rules guide validator (Stage 3)
        from tools.business_rules import init_guide_validator
        init_guide_validator(
            api_key=config.api_key,
            model=self.GUIDE_VALIDATOR_MODEL,
        )

        self.reset_conversation()

    def _get_tool_definitions(self) -> list[dict[str, Any]]:
        """Get tool definitions in OpenAI-compatible format."""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                },
            }
            for tool in self.tools.values()
        ]

    def _execute_tool(self, tool_call: ToolCall) -> str:
        """Execute a tool call and return the result as a string.

        Guaranteed to return a string, swallowing exceptions.

        For ``submit_answer``, a pre-submission verification step is run
        using a secondary LLM.  If the verifier finds issues, the SQL is
        **not** submitted; instead the feedback is returned so the agent
        can fix the query and retry within its normal iteration loop.
        After ``MAX_VERIFY_REJECTIONS`` consecutive rejections the query
        is submitted regardless to avoid infinite loops.
        """
        if tool_call.error:
            return f"Error parsing arguments for tool '{tool_call.name}': {tool_call.error}"

        if tool_call.name not in self.tools:
            return f"Error: Unknown tool '{tool_call.name}'"

        # ── Pre-submission verification gate ──
        if (
            tool_call.name == "submit_answer"
            and self._verify_rejections < self.MAX_VERIFY_REJECTIONS
        ):
            sql = tool_call.arguments.get("query", "")
            ctx = self._get_verification_context()
            result = self._verifier.verify(
                question=self._original_prompt,
                submitted_sql=sql,
                business_rules=ctx["business_rules"],
                schema_info=ctx["schema_info"],
            )
            if not result.passed:
                self._verify_rejections += 1
                return (
                    f"⚠ PRE-SUBMISSION VERIFICATION FAILED "
                    f"(attempt {self._verify_rejections}/"
                    f"{self.MAX_VERIFY_REJECTIONS}).\n"
                    "Your query was NOT submitted. Fix the issues "
                    "below, then call submit_answer again.\n\n"
                    f"{result.feedback}"
                )

        tool = self.tools[tool_call.name]
        try:
            return tool.function(**tool_call.arguments)
        except Exception as e:
            return f"Error executing {tool_call.name}: {e}"

    # -----------------------------------------------------------------
    # Verification helpers
    # -----------------------------------------------------------------

    def _get_verification_context(self) -> dict[str, str]:
        """Extract business rules and schema info from conversation history.

        Scans all tool-result messages and accumulates every
        ``get_business_rules`` response (there may be multiple calls for
        different domains) as well as every ``describe_table`` /
        ``list_schemas`` output, so the verifier has the same full context
        the agent used during this run.
        """
        rules_parts: list[str] = []
        schema_parts: list[str] = []

        for i, msg in enumerate(self.conversation.messages):
            if msg.role != "tool" or not msg.content:
                continue
            tool_name = self._tool_name_for_result(i)
            if tool_name == "get_business_rules" and not msg.content.startswith("No"):
                rules_parts.append(msg.content)
            elif tool_name in ("describe_table", "list_schemas"):
                schema_parts.append(msg.content)

        return {
            "business_rules": "\n\n---\n\n".join(rules_parts)[:6000],
            "schema_info": "\n".join(schema_parts)[:5000],
        }

    def _tool_name_for_result(self, tool_msg_index: int) -> str:
        """Given the index of a tool-result message, return the tool name."""
        target_id = self.conversation.messages[tool_msg_index].tool_call_id
        if not target_id:
            return ""
        for j in range(tool_msg_index - 1, -1, -1):
            tc_list = self.conversation.messages[j].tool_calls
            if self.conversation.messages[j].role == "assistant" and tc_list:
                for tc in tc_list:
                    if tc.get("id") == target_id:
                        return tc.get("function", {}).get("name", "")
                break
        return ""

    def _generate_response(self, conversation: Conversation) -> Iterator[AgentEvent]:
        """Generate a response from the model, streaming the events out."""
        yield AgentEvent(type=EventType.GENERATION_START)

        messages = conversation.to_api_format(compression=self._compression)
        tools = self._get_tool_definitions() if self.tools else None

        full_content = ""
        tool_calls: list[dict[str, Any]] = []
        in_thinking = False
        finish_reason: str | None = None
        usage: TokenUsage | None = None

        for chunk in self.client.chat_completion_stream(messages, tools):
            # Handle reasoning/thinking tokens
            if chunk.reasoning_details:
                for detail in chunk.reasoning_details:
                    if detail.get("type") == "reasoning.text":
                        text = detail.get("text", "")
                        if text:
                            if not in_thinking:
                                in_thinking = True
                                yield AgentEvent(type=EventType.THINKING_START)
                            yield AgentEvent(
                                type=EventType.THINKING_CHUNK,
                                data={"chunk": text},
                            )

            # Handle regular content
            if chunk.content:
                # Close thinking block if we were in it
                if in_thinking:
                    in_thinking = False
                    yield AgentEvent(type=EventType.THINKING_END)

                full_content += chunk.content
                yield AgentEvent(
                    type=EventType.RESPONSE_CHUNK,
                    data={"chunk": chunk.content},
                )

            # Handle tool calls (accumulated at the end)
            if chunk.tool_calls:
                tool_calls = chunk.tool_calls

            if chunk.finish_reason:
                finish_reason = chunk.finish_reason

            # Capture usage data (comes in final chunk)
            if chunk.usage:
                usage = chunk.usage

        # Close thinking if still open
        if in_thinking:
            yield AgentEvent(type=EventType.THINKING_END)

        event_data: dict[str, Any] = {
            "full_response": full_content,
            "tool_calls": tool_calls,
            "finish_reason": finish_reason,
        }
        if usage:
            event_data["usage"] = usage

        yield AgentEvent(type=EventType.GENERATION_END, data=event_data)

    def _get_system_message(self) -> str:  # noqa: PLR6301
        """Get the system message for the agent."""
        return (
            "You are an autonomous SQL agent working with a DuckDB "
            "database. You answer user questions by submitting a SQL "
            "query via the submit_answer tool.\n\n"
            #
            # ── WORKFLOW ──
            #
            "WORKFLOW — follow these steps in order for EVERY "
            "question:\n\n"
            "1. RETRIEVE BUSINESS RULES: Call get_business_rules "
            "with a keyword related to the question domain (e.g. "
            "the schema name, sport, industry, or topic). Read the "
            "returned rules **line by line** — they define critical "
            "filters, exclusions, thresholds, classifications, and "
            "calculations you MUST apply in your SQL. "
            "If the response ends with 'Other potentially relevant "
            "guides: ...' AND those guides seem related to the "
            "question, call get_business_rules again with one of "
            "those guide names to retrieve additional rules. A "
            "question spanning two domains (e.g. Airline + Finance) "
            "may need two separate calls.\n\n"
            "2. EXPLORE SCHEMA: Call list_schemas to see available "
            "schemas and tables. Then call describe_table for every "
            "relevant table to see the **exact** column names, "
            "types, and sample data. Always use the real column "
            "names you see in describe_table — never guess. "
            "If a business rule mentions a concept (e.g. 'delay', "
            "'carrier', 'on-time') and you are unsure which column "
            "holds it, call search_column with that keyword to find "
            "all matching columns across every table.\n\n"
            "3. GENERATE AND TEST SQL: Call generate_sql with the "
            "question, schema_info (from describe_table), and "
            "business_rules (from get_business_rules). Use the "
            "returned SQL in execute_sql to test it.\n"
            "   - If execute_sql returns an error, call generate_sql "
            "again with previous_sql and error_message to fix it.\n"
            "   - If results look wrong, call generate_sql again with "
            "updated context. You may iterate multiple times.\n\n"
            "4. PRE-SUBMISSION CHECK: Call check_sql with the "
            "question, your SQL, the business_rules text, and "
            "schema_info. If it reports issues, fix them and call "
            "check_sql again before submitting. Only skip check_sql "
            "if you have already been through a rejection cycle.\n\n"
            "5. SUBMIT: Once check_sql returns LGTM (or you have "
            "already addressed its feedback), call submit_answer.\n\n"
            #
            # ── APPLYING BUSINESS RULES ──
            #
            "APPLYING BUSINESS RULES (CRITICAL):\n\n"
            "After retrieving business rules, you MUST translate "
            "EVERY applicable rule into SQL. Go through each rule "
            "and ask: 'Does this rule apply to my query?' If yes, "
            "it MUST appear in your SQL as a WHERE filter, HAVING "
            "clause, CASE expression, or JOIN condition. Common "
            "patterns:\n\n"
            "a) EXCLUSION rules → add to WHERE clause.\n"
            "   When a rule says 'exclude X' or 'exclude rows where "
            "condition Y', add the corresponding WHERE condition.\n\n"
            "b) CLASSIFICATION rules → use CASE WHEN.\n"
            "   When a rule maps codes to labels (e.g. status A = "
            "'Good', B = 'Warning'), use CASE WHEN col = 'A' THEN "
            "'Good' WHEN col = 'B' THEN 'Warning' ... END.\n\n"
            "c) COMPLETED/ACTIVE-ENTITY rules → when rules say "
            "'only count completed' or 'exclude cancelled', add "
            "filters for non-null required fields and status flags.\n\n"
            "d) EXTERNAL-FACTOR exclusion → when rules say to "
            "exclude rows where an external factor is present "
            "(e.g. weather, system error), add the appropriate "
            "filter.\n\n"
            "e) THRESHOLD rules → rules like 'within N minutes' "
            "or 'over N hours' define exact thresholds. Use the "
            "exact column and threshold from the rules. "
            "'Within N' means <= N, not < N. Prefer columns that "
            "store non-negative values for thresholds.\n\n"
            "f) SUBTRACTION rules → when rules say to subtract "
            "refunds or reversals from gross amounts, use "
            "SUM(CASE WHEN ... THEN amt ELSE 0 END) - SUM(CASE "
            "WHEN ... THEN amt ELSE 0 END), not just exclude.\n\n"
            "g) DATE-CUTOFF rules → when rules mention legacy "
            "data, migration dates, or 'from year X onwards', add "
            "a date filter.\n\n"
            "h) MINIMUM-THRESHOLD rules → add to WHERE or HAVING "
            "depending on whether the threshold applies per row or "
            "to an aggregate.\n\n"
            #
            # ── OUTPUT FORMAT RULES ──
            #
            "OUTPUT FORMAT RULES:\n\n"
            "- Read the question carefully to identify EXACTLY "
            "which columns are requested.\n"
            "- If the question asks 'how many' or 'count', return "
            "a single COUNT(*) value, not the full list of rows.\n"
            "- Do NOT concatenate or merge columns unless the "
            "question explicitly asks. Keep first name and last "
            "name as separate columns.\n"
            "- When UNSURE whether a column is expected, INCLUDE "
            "it. Extra columns are NEVER penalized. Missing "
            "columns or wrong values ARE penalized.\n"
            "- Do NOT join to lookup/reference tables to resolve "
            "IDs to names UNLESS the question explicitly asks for "
            "names. If the question says 'by administrative unit' "
            "or 'by carrier', return the raw column value from "
            "the main table.\n"
            "- Do NOT add ORDER BY unless the question implies "
            "ordering (e.g. 'top N', 'highest', 'lowest', "
            "'ranked'). Unnecessary ORDER BY is harmless but "
            "unnecessary.\n"
            "- If the question asks for 'top N', always include "
            "ORDER BY ... DESC LIMIT N (or ASC for 'lowest').\n"
            "- Use COUNT(DISTINCT col) when counting unique "
            "entities that may appear in multiple rows.\n\n"
            #
            # ── NUMERIC PRECISION RULES ──
            #
            "NUMERIC PRECISION RULES (CRITICAL — wrong precision "
            "causes mismatches):\n\n"
            "- Do NOT apply ROUND() unless the question explicitly "
            "says 'round to N decimal places'. ROUND changes "
            "values and causes evaluation mismatches.\n"
            "- Return rates and ratios as FRACTIONS (0.0–1.0) "
            "using CAST(... AS REAL) / COUNT(*). Do NOT multiply "
            "by 100 UNLESS the question explicitly says "
            "'percentage' or 'percent'.\n"
            "- Use integer division (a / b) when context implies "
            "integers (e.g. counts, whole units). Use float "
            "division (CAST(x AS REAL) or x * 1.0) only when the "
            "context requires decimals.\n"
            "- NEVER wrap results in ROUND() 'just to be clean'. "
            "Raw computed values are expected.\n\n"
            #
            # ── FILTER RULES ──
            #
            "FILTER RULES:\n\n"
            "- Do NOT add WHERE col IS NOT NULL unless the "
            "question or business rules explicitly say to exclude "
            "NULLs. NULL values in GROUP BY create their own "
            "group, which is often the correct behavior.\n"
            "- Do NOT add extra WHERE filters beyond what the "
            "question and business rules specify. Every extra "
            "filter risks changing the row count.\n"
            "- When business rules say 'exclude status B from "
            "calculation', use NOT IN ('B') which covers ALL "
            "other statuses — do not enumerate them.\n\n"
            #
            # ── COLUMN NAME VERIFICATION ──
            #
            "COLUMN NAME VERIFICATION:\n\n"
            "After calling describe_table, copy the EXACT column "
            "names character-by-character into your query. Never "
            "guess. If the business rules mention a concept "
            "(e.g. delay, on-time, carrier), find the matching "
            "column in describe_table — similar-sounding columns "
            "may exist (e.g. delay vs delay_minutes) and have "
            "different semantics. Use the one that matches the "
            "rule's intent.\n\n"
            #
            # ── AGGREGATION RULES ──
            #
            "AGGREGATION vs ROW-LEVEL FILTERS:\n\n"
            "- When a threshold applies to an AGGREGATED measure "
            "(e.g. 'total X over a career', 'lifetime Y', "
            "'at least N total'), use HAVING on SUM/COUNT.\n"
            "  Example: 'at least 100 total X' →\n"
            "  HAVING SUM(x_col) >= 100  (NOT WHERE x_col >= 100)\n"
            "- When a threshold applies to individual rows "
            "(e.g. 'at least 50 X per record', 'per season'), "
            "use WHERE.\n"
            "- Think carefully: does the question refer to a "
            "per-row value or an aggregated total?\n\n"
            #
            # ── PRE-SUBMISSION CHECKLIST ──
            #
            "PRE-SUBMISSION CHECKLIST — verify ALL of these "
            "before calling submit_answer:\n\n"
            "1. COLUMNS: Does my SELECT include the columns the "
            "question asked for? Did I accidentally add ROUND() "
            "that wasn't requested? Did I multiply by 100 when "
            "the question didn't say 'percentage'?\n"
            "2. FILTERS: Did I apply every filter from the "
            "business rules? Did I add any extra filters NOT in "
            "the question or business rules (e.g. WHERE col IS "
            "NOT NULL, WHERE col != '')? Remove them.\n"
            "3. JOINS: Did I join to any table not needed for the "
            "requested output? If the question asks for an ID, "
            "do NOT join to get a name.\n"
            "4. ROW COUNT: Does the result row count make sense "
            "for the question? If it seems off, check filters.\n"
            "5. COLUMN NAMES: Am I using the exact column names "
            "from describe_table? No guessing.\n"
            "6. AGGREGATION: For threshold filters, am I using "
            "HAVING (for aggregated totals) vs WHERE (for "
            "per-row values) correctly?\n\n"
            #
            # ── GENERAL RULES ──
            #
            "GENERAL RULES:\n"
            "- Always use schema-qualified table names "
            "(e.g. SchemaName.TableName).\n"
            "- Apply ALL business rules from the guide — every "
            "filter, exclusion, and classification. Missing even "
            "one rule will produce wrong results.\n"
            "- If execute_sql returns an error, DO NOT submit that "
            "query. Fix it and test again.\n"
            "- NEVER stop without calling submit_answer.\n"
            "- Do not provide answers as plain text — always "
            "submit via submit_answer.\n\n"
            #
            # ── EXAMPLE 1 ──
            #
            "EXAMPLE 1 — Applying classification rules:\n\n"
            'User: "Show count and total by status classification."'
            "\n\n"
            'Step 1: get_business_rules("sales")\n'
            "  → Rules say: status A = Good, B = Warning, "
            "C/D = Bad.\n\n"
            "Step 2: list_schemas() → Sales schema.\n"
            "  describe_table(\"Sales\", \"orders\") → order_id, "
            "amount, status, ...\n\n"
            "Step 3: execute_sql(\n"
            "  \"SELECT\n"
            "     CASE WHEN status = 'A' THEN 'Good'\n"
            "          WHEN status = 'B' THEN 'Warning'\n"
            "          WHEN status IN ('C','D') THEN 'Bad'\n"
            "     END AS classification,\n"
            "     COUNT(*) AS cnt,\n"
            "     SUM(amount) AS total\n"
            "   FROM Sales.orders\n"
            "   GROUP BY classification\")\n"
            "  → 3 rows. Correct.\n\n"
            "Step 4: check_sql(question=..., sql=..., "
            "business_rules=..., schema_info=...)\n"
            "  → LGTM\n\n"
            "Step 5: submit_answer(query=\"SELECT CASE WHEN ...\")\n\n"
            #
            # ── EXAMPLE 2 ──
            #
            "EXAMPLE 2 — Applying exclusion and threshold rules:\n\n"
            'User: "Metric by category, excluding invalid rows."'
            "\n\n"
            'Step 1: get_business_rules("analytics")\n'
            "  → Rules say: exclude rows where flag = 1; use "
            "delay_min column for 'on-time' (<= 15).\n\n"
            "Step 2: describe_table(\"Analytics\", \"events\")\n"
            "  → Columns: category, delay_min, flag, ...\n"
            "  (Use delay_min, not delay_sec — check rules.)\n\n"
            "Step 3: execute_sql(\n"
            "  \"SELECT category,\n"
            "     SUM(CASE WHEN delay_min <= 15 THEN 1 ELSE 0 END) "
            "* 100.0 / COUNT(*) AS on_time_pct\n"
            "   FROM Analytics.events\n"
            "   WHERE flag != 1\n"
            "   GROUP BY category\")\n"
            "  → Results look correct.\n\n"
            "Step 4: check_sql(question=..., sql=..., "
            "business_rules=..., schema_info=...)\n"
            "  → LGTM\n\n"
            "Step 5: submit_answer(query=\"SELECT category, ...\")\n"
        )

    def run(self, prompt: str) -> Iterator[AgentEvent]:
        """Run the agent with streaming output, from the user's natural language prompt.

        Pre-submission verification is handled inside ``_execute_tool``:
        when the agent calls ``submit_answer``, a secondary LLM checks the
        SQL first.  If the check fails the agent receives feedback and
        continues its iteration loop to fix the query — no caller-side
        changes required.
        """
        # Remember the original prompt for the verifier and reset counter
        self._original_prompt = prompt
        self._verify_rejections = 0

        # Add the new user message to the ongoing conversation
        self.conversation.messages.append(Message(role="user", content=prompt))

        # Track cumulative token usage across all iterations
        total_usage = TokenUsage()

        for iteration in range(self.config.max_iterations):
            yield AgentEvent(type=EventType.ITERATION_START, data={"iteration": iteration + 1})

            full_response = ""
            tool_calls_data: list[dict[str, Any]] = []

            for event in self._generate_response(self.conversation):
                yield event
                if event.type == EventType.GENERATION_END:
                    full_response = event.data.get("full_response", "")
                    tool_calls_data = event.data.get("tool_calls", [])
                    # Accumulate token usage
                    if "usage" in event.data and event.data["usage"]:
                        total_usage = total_usage + event.data["usage"]

            # Parse tool calls from the structured response
            tool_calls = _parse_tool_calls_from_api(tool_calls_data)

            if not tool_calls:
                # Check if this is an empty response (model just stopped)
                is_empty_response = not full_response or not full_response.strip()

                # Check if response looks like a malformed tool call.
                # This happens when the model emits JSON-ish tool arguments
                # in assistant text instead of sending an actual tool call.
                looks_like_failed_tool_call = _looks_like_malformed_tool_call_text(
                    full_response,
                    set(self.tools.keys()),
                )

                if is_empty_response or looks_like_failed_tool_call:
                    # Model returned empty response or malformed tool call
                    # Inject a continuation prompt to remind it to properly call submit_answer
                    if looks_like_failed_tool_call:
                        print("\n[DEBUG] Response looks like failed tool call "
                              "- injecting continuation prompt")
                    else:
                        print("\n[DEBUG] Empty response detected "
                              "- injecting continuation prompt")

                    self.conversation.messages.append(
                        Message(role="assistant", content=full_response if full_response else "")
                    )
                    self.conversation.messages.append(
                        Message(
                            role="user",
                            content=(
                                "You must use the submit_answer TOOL to submit your "
                                "answer - do not output JSON directly. "
                                "Call the submit_answer tool now with your SQL query."
                            ),
                        )
                    )
                    # Continue to next iteration instead of returning
                    continue

                # Non-empty response without tool calls - agent is done
                self.conversation.messages.append(
                    Message(role="assistant", content=full_response)
                )
                yield AgentEvent(
                    type=EventType.AGENT_COMPLETE,
                    data={"response": full_response, "usage": total_usage},
                )
                return

            yield AgentEvent(type=EventType.TOOL_CALL_START, data={"count": len(tool_calls)})

            # Save assistant message with tool calls
            self.conversation.messages.append(
                Message(
                    role="assistant",
                    content=full_response if full_response else None,
                    tool_calls=tool_calls_data,
                )
            )

            for tool_call in tool_calls:
                yield AgentEvent(
                    type=EventType.TOOL_CALL_PARSED,
                    data={"name": tool_call.name, "arguments": tool_call.arguments},
                )
                yield AgentEvent(
                    type=EventType.TOOL_EXECUTION_START,
                    data={"name": tool_call.name},
                )
                tool_result = self._execute_tool(tool_call)
                yield AgentEvent(
                    type=EventType.TOOL_EXECUTION_END,
                    data={"name": tool_call.name, "result": tool_result},
                )

                # Add tool result message with tool_call_id
                self.conversation.messages.append(
                    Message(
                        role="tool",
                        content=tool_result,
                        tool_call_id=tool_call.id,
                    )
                )

                # Check if this tool signals agent completion (e.g., answer submitted)
                if tool_result.startswith(ANSWER_SUBMITTED_PREFIX):
                    yield AgentEvent(
                        type=EventType.AGENT_COMPLETE,
                        data={
                            "reason": "answer_submitted",
                            "tool": tool_call.name,
                            "usage": total_usage,
                        },
                    )
                    return

            yield AgentEvent(type=EventType.ITERATION_END, data={"iteration": iteration + 1})

        yield AgentEvent(
            type=EventType.AGENT_ERROR,
            data={"error": "Max iterations reached", "usage": total_usage},
        )

    def reset_conversation(self) -> None:
        """Reset the conversation to the initial state (with system message)."""
        self.conversation = Conversation()
        self.conversation.messages.append(
            Message(role="system", content=self._get_system_message())
        )


def _parse_tool_calls_from_api(tool_calls_data: list[dict[str, Any]]) -> list[ToolCall]:
    """Parse tool calls from OpenAI-compatible API response format."""
    tool_calls: list[ToolCall] = []

    for tc in tool_calls_data:
        tc_id = tc.get("id", "")
        function = tc.get("function", {})
        name = function.get("name", "")
        arguments_str = function.get("arguments", "{}")

        try:
            arguments = json.loads(arguments_str)
            error = None
        except json.JSONDecodeError as e:
            # Don't print to stdout, return error in ToolCall
            arguments = {}
            error = f"Invalid JSON arguments: {e}"

        tool_calls.append(
            ToolCall(
                id=tc_id,
                name=name,
                arguments=arguments,
                error=error,
            )
        )

    return tool_calls


def _looks_like_malformed_tool_call_text(
    text: str,
    tool_names: set[str],
) -> bool:
    """Heuristic detector for failed tool calls emitted as plain text.

    We only mark as malformed when the assistant output strongly resembles
    tool-call JSON, for example:
    - {"query": "..."}                        (raw arguments only)
    - {"name":"submit_answer","arguments":...} (tool envelope)
    - ```json { ... } ```                     (wrapped JSON)

    This avoids false positives from normal prose that merely contains "{"
    characters.
    """
    if not text or not text.strip():
        return False

    raw = text.strip()

    # Try to pull inner JSON from fenced block if present.
    if raw.startswith("```") and raw.endswith("```"):
        lines = raw.splitlines()
        if len(lines) >= 3:
            raw = "\n".join(lines[1:-1]).strip()

    if not (raw.startswith("{") and raw.endswith("}")):
        return False

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return False

    if not isinstance(payload, dict):
        return False

    keys = set(payload.keys())

    # Common "arguments-only" payload shape that should have been a tool call.
    arg_like_keys = {
        "query", "question", "sql", "schema_name", "table_name", "search_term",
        "keyword", "business_rules", "schema_info", "previous_sql", "error_message",
    }
    if keys and keys.issubset(arg_like_keys):
        return True

    # OpenAI-style tool envelope emitted as plain text.
    if "name" in payload and "arguments" in payload:
        name = str(payload.get("name", ""))
        if name in tool_names:
            return True

    if "tool" in payload and "arguments" in payload:
        name = str(payload.get("tool", ""))
        if name in tool_names:
            return True

    return False
