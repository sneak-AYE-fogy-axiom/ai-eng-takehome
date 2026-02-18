"""Tool for searching columns across all tables in the database.

Lets the agent find the exact column name, type, and table when it only
knows a concept (e.g. 'delay', 'carrier', 'status'). Uses DuckDB
information_schema so no LLM call is needed.
"""

from __future__ import annotations

from framework.agent import Tool
from framework.database import DATABASE_PATH

import duckdb

# Max columns to show in a single result to avoid flooding the context
_MAX_RESULTS = 40


def search_column(
    keyword: str,
    schema_name: str = "",
    table_name: str = "",
) -> str:
    """Search for columns across all schemas and tables whose name contains
    the given keyword (case-insensitive).

    Returns matching (schema, table, column, type) rows ranked by relevance:
    exact match > prefix match > substring match. Optional schema/table
    filters let the agent narrow the search once domain selection is known.

    Args:
        keyword: A word or partial word to match against column names
            (e.g. 'delay', 'carrier', 'status', 'amount').
        schema_name: Optional schema filter (case-insensitive contains match).
            Useful after list_schemas narrows the likely schema.
        table_name: Optional table filter (case-insensitive contains match).
            Useful after schema/table exploration narrows likely tables.

    Returns:
        Formatted string listing matching columns with their schema, table,
        type, and sample values.
    """
    if not keyword or not keyword.strip():
        return "Please provide a non-empty keyword."

    keyword_clean = keyword.strip()

    schema_filter = schema_name.strip()
    table_filter = table_name.strip()

    clauses: list[str] = ["LOWER(column_name) LIKE LOWER(?)"]
    params: list[str] = [f"%{keyword_clean}%"]
    if schema_filter:
        clauses.append("LOWER(table_schema) LIKE LOWER(?)")
        params.append(f"%{schema_filter}%")
    if table_filter:
        clauses.append("LOWER(table_name) LIKE LOWER(?)")
        params.append(f"%{table_filter}%")

    where_sql = " AND ".join(clauses)

    # Rank by match quality to reduce noise:
    #   3 = exact column name match
    #   2 = prefix match
    #   1 = substring match
    query = f"""
SELECT
    table_schema AS schema_name,
    table_name,
    column_name,
    data_type,
    CASE
        WHEN LOWER(column_name) = LOWER(?) THEN 3
        WHEN LOWER(column_name) LIKE LOWER(?) THEN 2
        ELSE 1
    END AS match_rank
FROM information_schema.columns
WHERE {where_sql}
ORDER BY
    match_rank DESC,
    table_schema,
    table_name,
    column_name
LIMIT {_MAX_RESULTS}
"""

    # Ranking params first, then WHERE params
    query_params = [keyword_clean, f"{keyword_clean}%"] + params

    conn: duckdb.DuckDBPyConnection | None = None
    try:
        conn = duckdb.connect(str(DATABASE_PATH), read_only=True)
        rows = conn.execute(query, query_params).fetchall()
    except Exception as e:
        return f"Search failed: {e}"
    finally:
        if conn is not None:
            conn.close()

    if not rows:
        return (
            f"No columns found matching '{keyword_clean}'. "
            "Try a shorter or different keyword."
        )

    lines: list[str] = [
        f"Columns matching '{keyword_clean}' "
        f"({len(rows)} result{'s' if len(rows) != 1 else ''}):",
        "",
        f"{'Schema':<22} {'Table':<40} {'Column':<35} {'Type':<20} Rank",
        "-" * 130,
    ]

    for row in rows:
        schema, table, col, dtype, rank = row
        lines.append(
            f"{str(schema):<22} {str(table):<40} {str(col):<35} {str(dtype):<20} {rank}"
        )

    if len(rows) == _MAX_RESULTS:
        lines.append(f"\n(Results capped at {_MAX_RESULTS}. Use a more specific keyword.)")

    if schema_filter or table_filter:
        lines.append(
            "\nApplied filters: "
            f"schema='{schema_filter or '*'}', table='{table_filter or '*'}'"
        )

    lines.append(
        "\nTo see sample values, call describe_table(schema_name, table_name)."
    )

    return "\n".join(lines)


SEARCH_COLUMN: Tool = Tool(
    name="search_column",
    description=(
        "Search for columns by keyword across ALL schemas and tables in the "
        "database. Use this when you know a concept (e.g. 'delay', 'carrier', "
        "'status', 'amount') but need to find the exact column name and which "
        "table it lives in. Results are ranked by relevance: exact > prefix > "
        "substring. Optional schema/table filters help narrow results. Returns "
        "schema, table, column name, and data type for every match. "
        "Follow up with describe_table to see sample values."
    ),
    parameters={
        "type": "object",
        "properties": {
            "keyword": {
                "type": "string",
                "description": (
                    "A word or partial word to search for in column names. "
                    "Examples: 'delay', 'carrier', 'status', 'amount', 'date'."
                ),
            },
            "schema_name": {
                "type": "string",
                "description": (
                    "Optional schema filter (case-insensitive contains match). "
                    "Example: 'Airline', 'financial'."
                ),
                "default": "",
            },
            "table_name": {
                "type": "string",
                "description": (
                    "Optional table filter (case-insensitive contains match). "
                    "Example: 'On_Time', 'charge'."
                ),
                "default": "",
            },
        },
        "required": ["keyword"],
    },
    function=search_column,
)
