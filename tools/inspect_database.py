"""Tool for inspecting database structure (schemas, tables, columns)."""

from framework.agent import Tool
from framework.database import (
    describe_table,
    list_schemas,
    list_tables,
)


def inspect_database(
    schema: str | None = None,
    table: str | None = None,
) -> str:
    """Inspect the database structure at various levels of detail.

    Args:
        schema: Optional schema name to inspect. If not provided, lists all schemas.
        table: Optional table name to inspect. Requires schema to be provided.
            If schema is provided but table is not, lists all tables in the schema.

    Returns:
        A formatted string describing the requested database structure.
    """
    # Case 1: Neither schema nor table provided - list all schemas
    if schema is None:
        schemas = list_schemas()
        if not schemas:
            return "No schemas found in the database."
        lines: list[str] = [f"Available schemas ({len(schemas)}):"]
        lines.extend(f"  - {s}" for s in schemas)
        return "\n".join(lines)

    # Case 2: Schema provided but table is not - list tables in schema
    if table is None:
        tables = list_tables(schema)
        if tables is None:
            return f"Schema '{schema}' not found."
        if not tables:
            return f"No tables found in schema '{schema}'."
        lines = [f"Tables in schema '{schema}' ({len(tables)}):"]
        lines.extend(f"  - {t}" for t in tables)
        return "\n".join(lines)

    # Case 3: Both schema and table provided - describe the table
    columns = describe_table(schema, table)
    if not columns:
        return f"Table '{schema}.{table}' not found or has no columns."
    lines = [f"Columns in '{schema}.{table}' ({len(columns)}):"]
    lines.extend(f"  - {col}" for col in columns)
    return "\n".join(lines)


INSPECT_DATABASE = Tool(
    name="inspect_database",
    description=(
        "Inspect the database structure. "
        "Call with no arguments to list all available schemas. "
        "Call with a schema name, but not table, to list all tables in that schema. "
        "Call with both schema and table to see the columns in that table. "
        "Use this tool when you want to understand the structure of the database, the "
        "schemas and tables available, or the columns (datatypes, etc) present on a "
        "specific table."
    ),
    parameters={
        "type": "object",
        "properties": {
            "schema": {
                "type": "string",
                "description": (
                    "The schema name to inspect. If not provided, lists all schemas."
                ),
            },
            "table": {
                "type": "string",
                "description": (
                    "The table name to describe. Requires schema to be provided. "
                    "If not provided (but schema is), lists all tables in the schema."
                ),
            },
        },
        "required": [],
    },
    function=inspect_database,
)
