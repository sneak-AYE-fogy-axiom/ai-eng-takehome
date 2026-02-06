"""Tool for executing SQL queries against the consolidated DuckDB database."""

import io
from functools import lru_cache

import polars
import tiktoken

from framework.agent import Tool
from framework.database import (
    QueryExecutionResult,
    execute_query,
    validate_query,
)

# Hard limit on rows returned to prevent excessive output
MAX_ROWS_HARD_LIMIT: int = 200

# Token limit for tool output to prevent context bloat
MAX_TOKENS_LIMIT: int = 4000


@lru_cache(maxsize=1)
def _get_encoder() -> tiktoken.Encoding:
    """Get the tiktoken encoder (cached for performance)."""
    return tiktoken.get_encoding("o200k_harmony")


def _count_tokens(text: str) -> int:
    """Count the number of tokens in a string."""
    return len(_get_encoder().encode(text))


def _format_result_csv(
    df: polars.DataFrame,
    num_rows: int,
    num_cols: int,
    rows_to_show: int,
    token_truncated: bool = False,
) -> str:
    """Format query results as CSV with metadata header.

    Args:
        df: The dataframe to format.
        num_rows: Total rows returned by the query.
        num_cols: Number of columns in the result.
        rows_to_show: Number of rows to include in the output.
        token_truncated: Whether rows were reduced due to token limit.

    Returns:
        Formatted string with metadata and CSV data.
    """
    lines: list[str] = []

    if rows_to_show >= num_rows:
        lines.append(f"Query returned {num_rows} row(s) and {num_cols} column(s).")
        display_df = df
    else:
        truncation_reason = "token limit" if token_truncated else "row limit"
        lines.append(
            f"Query returned {num_rows} row(s) and {num_cols} column(s). "
            f"Showing first {rows_to_show} rows (truncated due to {truncation_reason})."
        )
        display_df = df.head(rows_to_show)

    # Output as CSV for compact, LLM-friendly format
    lines.append("")  # Blank line before data
    csv_buffer = io.StringIO()
    display_df.write_csv(csv_buffer)
    lines.append(csv_buffer.getvalue().rstrip())

    return "\n".join(lines)


def run_sql(
    query: str,
    rows_to_display: int = 100,
) -> str:
    """Execute a SQL query against the database.

    Args:
        query: SQL query to execute. Use schema.table syntax (e.g., financial.account).
        rows_to_display: Maximum rows to include in output.
            Capped at MAX_ROWS_HARD_LIMIT.

    Returns:
        A string containing either:
        - CSV-formatted results with metadata on success
        - An error message describing what went wrong on failure
    """
    # Enforce hard limit on rows
    rows_to_display = min(rows_to_display, MAX_ROWS_HARD_LIMIT)

    # Step 1: Validate query syntax
    validation = validate_query(query)
    if not validation.is_valid:
        return f"SQL syntax error: {validation.error_message}"

    # Step 2: Execute the query
    result: QueryExecutionResult = execute_query(query)
    if not result.is_success:
        return f"Query execution failed: {result.error_message}"

    # Step 3: Format the successful result
    df = result.dataframe
    assert df is not None  # Guaranteed by is_success

    num_rows, num_cols = df.shape

    if result.is_empty:
        lines: list[str] = []
        lines.append("Query executed successfully but returned no data.")
        lines.append(f"Columns ({num_cols}): {', '.join(df.columns)}")
        return "\n".join(lines)

    # Determine initial row count (respecting row limit)
    rows_to_show = min(num_rows, rows_to_display)
    token_truncated = False

    # Generate initial output and check token count
    output = _format_result_csv(df, num_rows, num_cols, rows_to_show, token_truncated)
    token_count = _count_tokens(output)

    # If over token limit, progressively reduce rows until within limit
    # Use binary search for efficiency with large row counts
    if token_count > MAX_TOKENS_LIMIT and rows_to_show > 1:
        token_truncated = True
        low, high = 1, rows_to_show

        while low < high:
            mid = (low + high + 1) // 2  # Bias towards higher to maximize rows
            test_output = _format_result_csv(df, num_rows, num_cols, mid, token_truncated)
            if _count_tokens(test_output) <= MAX_TOKENS_LIMIT:
                low = mid
            else:
                high = mid - 1

        rows_to_show = low
        output = _format_result_csv(df, num_rows, num_cols, rows_to_show, token_truncated)

    return output


RUN_SQL = Tool(
    name="run_sql",
    description=(
        "Execute a SQL query against a database. The database dialect is DuckDB. "
        "You might want to inspect the database first to see what schemas are available. "
        "Similarly, you might want to look at the fields for a given table in a schema. "
        "Use schema.table syntax in your queries (e.g., SELECT * FROM financial.account). "
        "Always use full precision unless explicitly stated otherwise."
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "A SQL query to execute. Use schema.table syntax for table names "
                    "(e.g., 'SELECT * FROM financial.account WHERE ...')."
                ),
            },
            "rows_to_display": {
                "type": "integer",
                "description": (
                    "The maximum number of rows to display in the result. "
                    "Defaults to 100. Increase if you need to see more (max 200)."
                ),
                "default": 100,
            },
        },
        "required": ["query"],
    },
    function=run_sql,
)
