"""Tool that lets the agent proactively validate a SQL query before submission.

Unlike the silent pre-submission gate inside ``Agent._execute_tool``, this
tool is visible to the agent and can be called at any point — for example
after ``execute_sql`` returns results the agent is unsure about.  The agent
sees the critique and can decide to fix the query or proceed to submit.

Internally reuses the same ``Verifier`` logic so both checks are consistent.
"""

from __future__ import annotations

import logging

from framework.agent import Tool
from framework.verifier import Verifier

_logger = logging.getLogger(__name__)

# Module-level config (set via configure())
_api_key: str = ""
_verifier_model: str = ""


def configure(api_key: str, verifier_model: str = "moonshotai/kimi-k2.5") -> None:
    """Configure the check_sql tool with API key and model.

    Call this once before the tool is used (e.g. in create_tools).
    """
    global _api_key, _verifier_model  # noqa: PLW0603
    _api_key = api_key
    _verifier_model = verifier_model


def check_sql(
    question: str,
    sql: str,
    business_rules: str = "",
    schema_info: str = "",
) -> str:
    """Validate a SQL query against the question, business rules, and schema.

    Checks for common errors before submission:
    - Missing business rule filters or classifications
    - Wrong column names
    - Incorrect table / domain logic
    - Output format issues (concatenated names, missing columns)
    - Numeric precision issues (ROUND, percentages vs fractions)
    - Spurious WHERE filters or incorrect HAVING vs WHERE usage

    Args:
        question: The original natural-language question.
        sql: The SQL query to check.
        business_rules: The full business rules guide text (from
            get_business_rules). Pass everything returned by that tool.
        schema_info: Column descriptions from describe_table calls.
            Paste the relevant sections.

    Returns:
        "LGTM — no issues found." if the query looks correct, or a
        list of specific issues with suggested fixes if problems are found.
    """
    if not _api_key or not _verifier_model:
        return (
            "check_sql is not configured. "
            "Proceed with submit_answer if you are confident in your query."
        )

    verifier = Verifier(api_key=_api_key, model=_verifier_model)
    result = verifier.verify(
        question=question,
        submitted_sql=sql,
        business_rules=business_rules,
        schema_info=schema_info,
    )

    if result.passed:
        return "LGTM — no issues found. You may call submit_answer with this query."

    return (
        "Issues found — fix these before submitting:\n\n"
        + result.feedback
    )


CHECK_SQL: Tool = Tool(
    name="check_sql",
    description=(
        "Validate a SQL query before submitting it. "
        "Checks that all applicable business rules are implemented, "
        "that column names are correct, that output format matches the "
        "question, and that numeric precision is right. "
        "Call this after execute_sql looks correct but before submit_answer "
        "when you want a second opinion. "
        "Pass the question, your SQL, the business_rules text from "
        "get_business_rules, and the schema_info from describe_table."
    ),
    parameters={
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The original natural-language question.",
            },
            "sql": {
                "type": "string",
                "description": "The SQL query to validate.",
            },
            "business_rules": {
                "type": "string",
                "description": (
                    "Full business rules text from get_business_rules. "
                    "Paste the entire returned content."
                ),
                "default": "",
            },
            "schema_info": {
                "type": "string",
                "description": (
                    "Column descriptions from describe_table calls. "
                    "Paste the relevant parts."
                ),
                "default": "",
            },
        },
        "required": ["question", "sql"],
    },
    function=check_sql,
)
