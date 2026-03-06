from fastapi import APIRouter, HTTPException
from ..schemas import QueryRequest, QueryResponse, SchemasResponse
from ..services.llm_service import generate_sql
from ..services.sql_service import execute_sql
from ..services.chart_service import suggest_chart
from ..database import get_all_schemas

router = APIRouter()


@router.get("/schemas", response_model=SchemasResponse)
def list_schemas():
    """Return all schemas and their tables for the frontend schema browser."""
    try:
        schemas = get_all_schemas()
        return SchemasResponse(schemas=schemas)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/query", response_model=QueryResponse)
def run_query(req: QueryRequest):
    """Accept a natural language question and return SQL, data, and optional chart config."""
    try:
        sql_query = generate_sql(req.question, req.schema)
        data = execute_sql(sql_query)
        chart = suggest_chart(data)
        return QueryResponse(sql=sql_query, data=data, chart=chart)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
