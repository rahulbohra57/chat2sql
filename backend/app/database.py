from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# System schemas to always exclude from the browser and LLM context
_SYSTEM_SCHEMAS = (
    "information_schema", "pg_catalog", "pg_toast",
    "auth", "extensions", "graphql", "graphql_public",
    "pgbouncer", "realtime", "storage", "vault",
)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _user_schema_filter() -> str:
    """Build SQL fragment that excludes all system schemas and pg_* prefixes."""
    excluded = ", ".join(f"'{s}'" for s in _SYSTEM_SCHEMAS)
    return f"c.table_schema NOT IN ({excluded}) AND c.table_schema NOT LIKE 'pg_%'"


def _fetch_columns(schema: str | None = None) -> list[tuple]:
    if schema:
        where = f"c.table_schema = '{schema}'"
    else:
        where = _user_schema_filter()

    query = text(f"""
        SELECT
            c.table_schema,
            c.table_name,
            c.column_name,
            c.data_type
        FROM information_schema.columns c
        JOIN information_schema.tables t
            ON c.table_name  = t.table_name
            AND c.table_schema = t.table_schema
        WHERE {where}
          AND t.table_type = 'BASE TABLE'
        ORDER BY c.table_schema, c.table_name, c.ordinal_position
    """)
    with engine.connect() as conn:
        return conn.execute(query).fetchall()


def get_schema_info(schema: str | None = None) -> str:
    """
    Return a plain-text description of tables/columns for the LLM prompt.
    Scoped to `schema` if given, otherwise all user schemas.
    """
    rows = _fetch_columns(schema)

    if not rows:
        return "No tables found in the database."

    lines = []
    current = None
    for table_schema, table_name, column_name, data_type in rows:
        qualified = f"{table_schema}.{table_name}"
        if qualified != current:
            if current is not None:
                lines.append("")
            lines.append(f"Table: {qualified}")
            lines.append("Columns:")
            current = qualified
        lines.append(f"  - {column_name} ({data_type})")

    return "\n".join(lines)


def get_all_schemas() -> list[dict]:
    """
    Return structured schema info for the frontend schema browser.
    Automatically includes every user schema — no hardcoded list needed.
    """
    rows = _fetch_columns()

    schemas: dict[str, dict[str, list]] = {}
    for table_schema, table_name, column_name, data_type in rows:
        schemas.setdefault(table_schema, {}).setdefault(table_name, []).append(
            {"name": column_name, "type": data_type}
        )

    return [
        {
            "name": schema_name,
            "tables": [
                {"name": tname, "columns": cols}
                for tname, cols in tables.items()
            ],
        }
        for schema_name, tables in schemas.items()
    ]
