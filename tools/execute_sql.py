"""Tool for executing SQL queries against the DuckDB database.

Allows the agent to test queries before submitting, with syntax validation
and formatted output including row limits to prevent token explosion.
"""

from framework.agent import Tool
from framework.database import execute_query, validate_query

MAX_DISPLAY_ROWS = 50


def execute_sql(query: str) -> str:
    """Execute a SQL query and return formatted results or an error message.

    Args:
        query: SQL query with schema-qualified table names.

    Returns:
        Formatted results string, or an error message if validation/execution fails.
    """
    # Step 1: Syntax validation via sqlglot
    validation = validate_query(query)
    if not validation.is_valid:
        return (
            f"SQL SYNTAX ERROR: {validation.error_message}\n"
            "Please fix the query and try again."
        )

    # Step 2: Execute against DuckDB
    result = execute_query(query)
    if not result.is_success:
        return (
            f"EXECUTION ERROR: {result.error_message}\n"
            "Please fix the query and try again."
        )

    # Step 3: Format results
    df = result.dataframe
    if df is None:
        return "Query executed successfully but returned no dataframe."

    if df.is_empty():
        col_info = ", ".join(df.columns)
        return f"Query returned 0 rows.\nColumns: {col_info}"

    total_rows = df.height
    total_cols = df.width

    # Build header
    lines: list[str] = [
        f"Results: {total_rows} rows x {total_cols} columns",
        "",
    ]

    # Display up to MAX_DISPLAY_ROWS
    display_df = df.head(MAX_DISPLAY_ROWS)

    # Column headers
    col_names = display_df.columns
    header = " | ".join(col_names)
    separator = "-+-".join("-" * max(len(c), 8) for c in col_names)
    lines.append(header)
    lines.append(separator)

    # Data rows
    for row in display_df.rows():
        row_str = " | ".join(str(v) if v is not None else "NULL" for v in row)
        lines.append(row_str)

    if total_rows > MAX_DISPLAY_ROWS:
        lines.append(f"... ({total_rows - MAX_DISPLAY_ROWS} more rows not shown)")

    return "\n".join(lines)


EXECUTE_SQL: Tool = Tool(
    name="execute_sql",
    description=(
        "Execute a SQL query against the DuckDB database and see the results. "
        "Use this to explore data and test your queries before submitting. "
        "Table names must be schema-qualified (e.g., 'SELECT * FROM Airline.flights LIMIT 5'). "
        "If the query has errors, the error message will be returned so you can fix and retry."
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "The SQL query to execute. Must use schema-qualified table names "
                    "(e.g., 'schema.table'). Use LIMIT to avoid large result sets."
                ),
            },
        },
        "required": ["query"],
    },
    function=execute_sql,
)
