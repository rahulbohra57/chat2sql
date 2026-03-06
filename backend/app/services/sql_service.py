import re
from fastapi import HTTPException
from sqlalchemy import text
from ..database import engine

DESTRUCTIVE_PATTERN = re.compile(
    r"\b(DELETE|UPDATE|DROP|INSERT|TRUNCATE|ALTER|CREATE|REPLACE|MERGE)\b",
    re.IGNORECASE,
)

ROW_LIMIT = 500


def validate_sql(sql: str) -> None:
    """Raise HTTPException if the SQL contains destructive keywords."""
    match = DESTRUCTIVE_PATTERN.search(sql)
    if match:
        raise HTTPException(
            status_code=400,
            detail=f"Query blocked: '{match.group()}' statements are not allowed.",
        )


def execute_sql(sql: str) -> list[dict]:
    """
    Validate and execute a SQL query against the database.
    Returns a list of row dicts, capped at ROW_LIMIT rows.
    """
    validate_sql(sql)

    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            columns = list(result.keys())
            rows = result.fetchmany(ROW_LIMIT)
            return [dict(zip(columns, row)) for row in rows]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"SQL execution error: {str(exc)}")
