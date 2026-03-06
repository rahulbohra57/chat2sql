from pydantic import BaseModel
from typing import Any


class QueryRequest(BaseModel):
    question: str
    schema: str | None = None  # e.g. "hr" or "public"; None = all schemas


class QueryResponse(BaseModel):
    sql: str
    data: list[dict[str, Any]]
    chart: dict[str, Any] | None = None
    error: str | None = None


class ColumnInfo(BaseModel):
    name: str
    type: str


class TableInfo(BaseModel):
    name: str
    columns: list[ColumnInfo]


class SchemaInfo(BaseModel):
    name: str
    tables: list[TableInfo]


class SchemasResponse(BaseModel):
    schemas: list[SchemaInfo]
