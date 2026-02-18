"""Tools for discovering database schema structure.

Provides two tools:
- list_schemas: Lists all schemas and their tables
- describe_table: Shows column details and sample data for a specific table
"""

from framework.agent import Tool
from framework.database import (
    describe_table as db_describe_table,
)
from framework.database import (
    execute_query,
)
from framework.database import (
    list_schemas as db_list_schemas,
)
from framework.database import (
    list_tables as db_list_tables,
)


def list_schemas() -> str:
    """List all available schemas and their tables.

    Returns:
        Formatted string showing each schema and its tables.
    """
    schemas = db_list_schemas()
    if not schemas:
        return "No schemas found in the database."

    lines: list[str] = [f"Available schemas ({len(schemas)} total):", ""]

    for schema in schemas:
        tables = db_list_tables(schema)
        if tables:
            table_list = ", ".join(tables)
            lines.append(f"  {schema}: {table_list}")
        else:
            lines.append(f"  {schema}: (no tables)")

    return "\n".join(lines)


def describe_table(schema_name: str, table_name: str) -> str:
    """Describe a table's columns and show sample data.

    Args:
        schema_name: Name of the schema (e.g., 'Airline').
        table_name: Name of the table (e.g., 'On_Time_On_Time_Performance_2016_1').

    Returns:
        Formatted string with column info and sample rows.
    """
    columns = db_describe_table(schema_name, table_name)
    if not columns:
        return f"Table '{schema_name}.{table_name}' not found or has no columns."

    lines: list[str] = [
        f"Table: {schema_name}.{table_name}",
        f"Columns ({len(columns)}):",
    ]
    for col in columns:
        lines.append(f"  - {col}")

    # Fetch 3 sample rows for context
    sample_result = execute_query(
        f'SELECT * FROM "{schema_name}"."{table_name}" LIMIT 3'
    )
    if sample_result.is_success and sample_result.dataframe is not None:
        df = sample_result.dataframe
        if not df.is_empty():
            lines.append("")
            lines.append("Sample data (3 rows):")
            col_names = df.columns
            lines.append(" | ".join(col_names))
            lines.append("-+-".join("-" * max(len(c), 8) for c in col_names))
            for row in df.rows():
                row_str = " | ".join(
                    str(v) if v is not None else "NULL" for v in row
                )
                lines.append(row_str)

    return "\n".join(lines)


LIST_SCHEMAS: Tool = Tool(
    name="list_schemas",
    description=(
        "List all available database schemas and their tables. "
        "Call this to discover which schemas and tables exist in the database. "
        "No parameters required."
    ),
    parameters={
        "type": "object",
        "properties": {},
    },
    function=list_schemas,
)

DESCRIBE_TABLE: Tool = Tool(
    name="describe_table",
    description=(
        "Get detailed column information and sample data for a specific table. "
        "Use this to understand table structure before writing queries."
    ),
    parameters={
        "type": "object",
        "properties": {
            "schema_name": {
                "type": "string",
                "description": "The schema name (e.g., 'Airline', 'Credit', 'financial').",
            },
            "table_name": {
                "type": "string",
                "description": "The table name within the schema.",
            },
        },
        "required": ["schema_name", "table_name"],
    },
    function=describe_table,
)
