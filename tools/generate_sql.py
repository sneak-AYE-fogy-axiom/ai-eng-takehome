"""Tool for generating SQL via a dedicated NL2SQL model (e.g. anthropic/claude-opus-4.6).

The main agent uses minimax for tool call and routing; this tool delegates
SQL generation to a specialized model for better accuracy.
"""

from __future__ import annotations

import logging
import re

from framework.agent import Tool
from framework.llm import completion_request

_logger = logging.getLogger(__name__)

# Module-level config (set by create_tools)
_api_key: str = ""
_nl2sql_model: str = ""


def configure(api_key: str, nl2sql_model: str) -> None:
    """Configure the generate_sql tool with API key and model.

    Call this before the tool is used (e.g. in create_tools).
    """
    global _api_key, _nl2sql_model  # noqa: PLW0603
    _api_key = api_key
    _nl2sql_model = nl2sql_model


def _extract_sql_from_response(text: str) -> str:
    """Extract SQL from model response, handling markdown code blocks."""
    text = text.strip()
    # Try to find ```sql ... ``` or ``` ... ```
    match = re.search(r"```(?:sql)?\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # If no block, assume the whole response is SQL (trim common prefixes)
    for prefix in ("SELECT", "WITH", "INSERT", "UPDATE", "DELETE"):
        if text.upper().startswith(prefix):
            return text
    return text


def generate_sql(
    question: str,
    schema_info: str = "",
    business_rules: str = "",
    previous_sql: str = "",
    error_message: str = "",
) -> str:
    """Generate a SQL query for the given question using the NL2SQL model.

    Args:
        question: The user's natural language question.
        schema_info: Relevant schema (tables, columns) from list_schemas/describe_table.
        business_rules: Relevant business rules from get_business_rules.
        previous_sql: Previous SQL attempt (for retries).
        error_message: Error from execute_sql (for retries).

    Returns:
        The generated SQL query, or an error message if generation fails.
    """
    if not _api_key or not _nl2sql_model:
        return (
            "Error: generate_sql is not configured (missing api_key or nl2sql_model). "
            "Use execute_sql with your own SQL instead."
        )

    system_prompt = (
        "You are a DuckDB SQL expert. Generate a single SQL query that answers "
        "the user's question. Use schema-qualified table names (Schema.Table). "
        "Return ONLY the SQL query — no explanation, no markdown fences.\n\n"
        "RULES — YOU MUST FOLLOW ALL OF THESE:\n\n"
        "1. BUSINESS RULES APPLICATION: When business rules are provided, "
        "translate EVERY applicable rule into SQL:\n"
        "   - Exclusion rules → WHERE filters (e.g. WHERE status NOT IN ('X'))\n"
        "   - Classification mappings → CASE WHEN col = 'A' THEN 'Label' END\n"
        "   - Completed-only rules → WHERE completed_col IS NOT NULL\n"
        "   - External-factor exclusions → WHERE factor_col IS NULL OR factor_col = 0\n"
        "   - Threshold rules → use the exact column and threshold from the rules\n"
        "   - Date-cutoff rules → WHERE date_col >= 'YYYY-01-01'\n"
        "   - Min-threshold on aggregates → HAVING SUM/COUNT >= N\n"
        "   - Subtraction rules → SUM(CASE WHEN type='refund' THEN -amt ELSE amt END)\n\n"
        "2. COLUMN NAMES: Use ONLY exact column names from the schema. "
        "Never guess. If similar-sounding columns exist, choose the one "
        "that matches the rule's intent.\n\n"
        "3. NUMERIC PRECISION:\n"
        "   - Do NOT add ROUND() unless the question says 'round to N places'\n"
        "   - Return fractions (0.0–1.0) unless the question says 'percentage'\n"
        "   - Use CAST(x AS REAL) or x * 1.0 for float division when needed\n\n"
        "4. FILTERS:\n"
        "   - Do NOT add WHERE col IS NOT NULL unless explicitly required\n"
        "   - Do NOT add extra filters beyond what the question and rules say\n\n"
        "5. OUTPUT:\n"
        "   - Keep name fields as separate columns (do not concatenate)\n"
        "   - Include ALL columns the question asks for\n"
        "   - Add ORDER BY only when the question implies ranking/top-N\n"
        "   - Use HAVING for aggregate thresholds, WHERE for row-level\n"
    )

    user_parts: list[str] = [f"Question: {question}"]

    if schema_info:
        user_parts.append(f"\nSchema:\n{schema_info}")
    if business_rules:
        user_parts.append(f"\nBusiness rules (MUST apply):\n{business_rules}")
    if previous_sql and error_message:
        user_parts.append(
            f"\nPrevious attempt failed:\nSQL: {previous_sql}\nError: {error_message}\n"
            "Fix the SQL and return the corrected query."
        )

    user_content = "\n".join(user_parts)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]

    try:
        response = completion_request(
            api_key=_api_key,
            model=_nl2sql_model,
            messages=messages,
            temperature=0.2,
        )
        sql = _extract_sql_from_response(response)
        if not sql:
            return "Error: Model returned empty SQL."
        return sql
    except Exception as e:
        _logger.warning("generate_sql failed: %s", e, exc_info=True)
        return f"Error generating SQL: {e}"


def create_generate_sql_tool() -> Tool:
    """Create the generate_sql tool. Call configure() first."""
    return Tool(
        name="generate_sql",
        description=(
            "Generate a SQL query for the user's question using a specialized "
            "NL2SQL model. Call this when you need to write SQL — pass the "
            "question, schema info (from describe_table), and business rules "
            "(from get_business_rules). Use the returned SQL in execute_sql to "
            "test, then submit_answer when correct. For retries after errors, "
            "pass previous_sql and error_message."
        ),
        parameters={
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The user's natural language question.",
                },
                "schema_info": {
                    "type": "string",
                    "description": (
                        "Relevant schema (tables, columns) from list_schemas "
                        "and describe_table. Paste the key parts."
                    ),
                    "default": "",
                },
                "business_rules": {
                    "type": "string",
                    "description": (
                        "Relevant business rules from get_business_rules. "
                        "Paste the full or summarized rules."
                    ),
                    "default": "",
                },
                "previous_sql": {
                    "type": "string",
                    "description": "Previous SQL that failed (for retries).",
                    "default": "",
                },
                "error_message": {
                    "type": "string",
                    "description": "Error from execute_sql (for retries).",
                    "default": "",
                },
            },
            "required": ["question"],
        },
        function=generate_sql,
    )
