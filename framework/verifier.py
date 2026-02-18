"""Pre-submission SQL query verifier using a secondary LLM model.

Called inside the agent's ``_execute_tool`` method, *before* the actual
``submit_answer`` tool fires.  If the verifier detects issues, the SQL is
not submitted — the feedback is returned to the agent so it can fix the
query and retry within its normal iteration loop.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from framework.llm import completion_request

_logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Verifier system prompt — derived from error-pattern analysis but kept
# generic so it does not overfit to any particular evaluation question.
# ---------------------------------------------------------------------------

_VERIFIER_SYSTEM_PROMPT = """\
You are a SQL query verifier for a DuckDB database. Your job is to check \
whether a submitted SQL query will return the correct results for a given \
natural-language question, according to the provided business rules and \
schema information.

You will receive four inputs:
1. The original question
2. The business rules guide that applies to this domain
3. Schema information (column names, types, sample rows)
4. The submitted SQL query

Examine the query for the following error patterns:

## 1. BUSINESS RULES COMPLETENESS
Every applicable rule from the guide MUST appear in the SQL. For each rule \
ask: "Does this rule apply to the question?" If yes, verify it is \
implemented — as a WHERE filter, HAVING clause, CASE expression, or JOIN \
condition. Commonly missed rules include:
- Exclusion rules (certain rows, statuses, or transaction types must be \
filtered out)
- Entities that must be reported separately or excluded entirely
- Classification mappings that should produce human-readable labels via \
CASE WHEN instead of returning raw codes
- Minimum-threshold or minimum-count requirements
- Date or period restrictions (legacy data cutoffs, era boundaries)

## 2. COLUMN CORRECTNESS
Every column name in the SQL must match a real column from the schema info. \
Watch for:
- Similarly-named columns with different semantics (e.g., one column is \
always non-negative while another can be negative; one is a code, another \
a full identifier)
- Using the wrong column for threshold checks or aggregation

## 3. TABLE SELECTION AND DOMAIN LOGIC
- Detail tables (individual records) are usually correct when filters must \
be applied. Summary or aggregate tables may lack the columns needed for \
filtering and should be avoided in those cases.
- Metrics should be calculated from raw data columns; using pre-computed \
columns can give wrong results when combined with WHERE filters.
- Domain concepts (e.g., "completed", "on-time", "default", "rookie") \
must match the definitions in the business rules, not general intuition.

## 4. OUTPUT FORMAT
- Does the SELECT list include ALL columns the question asks for?
- Are person names kept as separate columns (not concatenated)?
- When the question refers to a classification, does the query use \
CASE WHEN labels from the business rules, or raw codes?
- If the question implies a constant/literal label column (e.g., "as a \
single 'Region X' entity"), is it present?

## 5. NUMERIC PRECISION
- ROUND() only if the question explicitly says "round to N places".
- Rates/ratios as fractions (0–1) unless the question says "percentage".
- Integer division vs float division should match context expectations.

## 6. FILTER CORRECTNESS
- No extra WHERE filters that are not justified by the question or rules \
(e.g., unnecessary IS NOT NULL that removes valid data).
- HAVING for aggregated thresholds (career totals, lifetime sums) vs \
WHERE for per-row thresholds.
- No unnecessary table joins that could change the result count.

RESPOND WITH EXACTLY ONE OF:
- "PASS" — if the query is correct
- "FAIL:" followed by each issue on its own line — if there are problems. \
Be specific about what is wrong and what the correct fix should be.
"""


@dataclass
class VerifierResult:
    """Result of a verification check."""

    passed: bool
    feedback: str


class Verifier:
    """Verifies submitted SQL queries using a secondary LLM model.

    Uses a non-streaming completion call to a separate model so that the
    verification is independent of the primary agent model.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "moonshotai/kimi-k2.5",
    ) -> None:
        self._api_key = api_key
        self._model = model

    def verify(
        self,
        question: str,
        submitted_sql: str,
        business_rules: str,
        schema_info: str,
    ) -> VerifierResult:
        """Verify a submitted SQL query against question and context.

        Args:
            question: The original natural-language question.
            submitted_sql: The SQL query to verify.
            business_rules: Business rules guide content.
            schema_info: Schema / table descriptions from describe_table.

        Returns:
            VerifierResult indicating pass or fail with feedback.
        """
        user_content = (
            f"## Original Question\n{question}\n\n"
            f"## Business Rules Guide\n"
            f"{business_rules[:4000] if business_rules else '(none retrieved)'}\n\n"
            f"## Schema Information\n"
            f"{schema_info[:4000] if schema_info else '(none retrieved)'}\n\n"
            f"## Submitted SQL Query\n```sql\n{submitted_sql}\n```"
        )

        messages = [
            {"role": "system", "content": _VERIFIER_SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ]

        try:
            response = completion_request(
                api_key=self._api_key,
                model=self._model,
                messages=messages,
                temperature=0.1,
            )
        except Exception:
            _logger.warning(
                "Verifier call failed; treating as PASS", exc_info=True,
            )
            return VerifierResult(passed=True, feedback="")

        response_stripped = response.strip()

        if response_stripped.upper().startswith("PASS"):
            return VerifierResult(passed=True, feedback="")

        # Extract feedback after optional "FAIL:" prefix
        feedback = response_stripped
        if feedback.upper().startswith("FAIL:"):
            feedback = feedback[5:].strip()

        return VerifierResult(passed=False, feedback=feedback)
