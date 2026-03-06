import re
import google.generativeai as genai
from ..config import GEMINI_API_KEY, GEMINI_MODEL
from ..database import get_schema_info

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT_TEMPLATE = """You are a PostgreSQL expert.
Convert the user's natural language question into a valid SQL SELECT query.

Rules:
- Only return the SQL query, nothing else
- Use valid PostgreSQL syntax
- Never include explanations, markdown, or code fences
- Never generate DELETE, UPDATE, DROP, INSERT, TRUNCATE, or ALTER statements
- Always use SELECT statements only
- Limit results to 500 rows using LIMIT unless the user specifies otherwise

Database schema:
{schema}
"""


def generate_sql(question: str, schema: str | None = None) -> str:
    """
    Convert a natural language question to SQL using the Gemini model
    configured in GEMINI_MODEL env var. Swap the env var to rotate models
    without touching any other file.
    """
    schema_info = get_schema_info(schema)
    prompt = SYSTEM_PROMPT_TEMPLATE.format(schema=schema_info) + f"\n\nUser question: {question}"

    model = genai.GenerativeModel(GEMINI_MODEL)
    try:
        response = model.generate_content(prompt)
    except Exception as exc:
        error_str = str(exc)
        # Surface a clean quota / auth message instead of the raw proto dump
        if "429" in error_str or "quota" in error_str.lower():
            raise RuntimeError(
                f"Gemini quota exceeded for model '{GEMINI_MODEL}'. "
                "Change GEMINI_MODEL in .env (e.g. gemini-1.5-pro) or rotate GEMINI_API_KEY."
            )
        if "401" in error_str or "api_key" in error_str.lower():
            raise RuntimeError("Invalid GEMINI_API_KEY. Check your .env file.")
        raise

    sql = response.text.strip()

    # Strip markdown code fences if the model wraps the SQL
    sql = re.sub(r"^```(?:sql)?\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\s*```$", "", sql)

    return sql.strip()
