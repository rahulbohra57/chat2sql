# Chat2SQL — AI SQL Analyst

> **Live App:** [https://chat2sql-frontend.onrender.com](https://chat2sql-frontend.onrender.com)
> **API:** [https://chat2sql-backend.onrender.com](https://chat2sql-backend.onrender.com)

Ask questions about your PostgreSQL database in plain English. Powered by Google Gemini, FastAPI, and Next.js.

---

## What It Does

Type a question like *"Show top 5 employees by salary"* and the system:

1. Introspects your database schema automatically
2. Sends the schema + your question to Gemini AI
3. Generates a valid PostgreSQL query
4. Executes it safely against the database
5. Returns results as a table + bar chart
6. Shows the generated SQL below the results

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16, TypeScript, Recharts |
| Backend | FastAPI, Python 3.11, SQLAlchemy |
| Database | Supabase PostgreSQL |
| AI | Google Gemini (configurable model) |
| Deployment | Render |

---

## Features

- Natural language → SQL via Gemini AI
- Schema browser — visual sidebar showing all schemas, tables, and columns
- Schema switcher — query `hr`, `ecommerce`, `school`, or all at once
- Auto-discovers schemas — add new schemas and they appear instantly, no config needed
- Bar chart visualization — auto-generated when results have a label + numeric column
- SQL transparency — generated query shown below results
- Security — blocks `DELETE`, `UPDATE`, `DROP`, `INSERT`, `TRUNCATE`, `ALTER`; results capped at 500 rows
- Configurable AI model — swap Gemini model in `.env` without touching code

---

## Sample Schemas (Pre-loaded)

| Schema | Tables |
|--------|--------|
| `hr` | employees, departments, jobs, locations, countries, regions, job_history |
| `ecommerce` | customers, products, categories, orders, order_items, reviews |
| `school` | students, teachers, courses, departments, enrollments, grades |

### Example Questions to Try

```
hr schema
  Who earns the highest salary?
  List all employees in the Sales department
  Which department has the most employees?
  Show average salary by job title

ecommerce schema
  Which product has the highest rating?
  Show top 5 customers by total order amount
  What is the revenue by product category?
  List all pending orders

school schema
  Which student has the highest average marks?
  Show course enrollment counts
  List all teachers and their departments
  Which course has the most students enrolled?
```

---

## Local Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- A Supabase project (or any PostgreSQL database)
- A Google Gemini API key — https://aistudio.google.com/app/apikey

### 1. Clone the repo

```bash
git clone https://github.com/rahulbohra57/chat2sql.git
cd chat2sql
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
DATABASE_URL=postgresql+psycopg2://postgres.<ref>:<password>@<host>.pooler.supabase.com:5432/postgres
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-flash
```

> To rotate keys: only change `GEMINI_API_KEY`.
> To switch models: change `GEMINI_MODEL` — options: `gemini-1.5-flash`, `gemini-1.5-pro`, `gemini-2.0-flash`

### 3. Seed the database (optional)

Run `seed.sql` in your Supabase SQL editor to create the HR demo schema.

### 4. Start the backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
# API at http://localhost:8000
```

### 5. Start the frontend

```bash
cd frontend
npm install
npm run dev
# App at http://localhost:3000
```

---

## API Reference

### `GET /schemas`

Returns all user schemas, tables, and columns.

```json
{
  "schemas": [
    {
      "name": "hr",
      "tables": [
        { "name": "employees", "columns": [{"name": "employee_id", "type": "integer"}] }
      ]
    }
  ]
}
```

### `POST /query`

Converts a question to SQL and returns results.

**Request:**
```json
{ "question": "Show top 5 employees by salary", "schema": "hr" }
```

**Response:**
```json
{
  "sql": "SELECT first_name, last_name, salary FROM hr.employees ORDER BY salary DESC LIMIT 5",
  "data": [...],
  "chart": { "type": "bar", "labels": [...], "values": [...] },
  "error": null
}
```

---

## Deploy to Render

### Backend

1. Render Dashboard → New → Web Service → connect `rahulbohra57/chat2sql`
2. Root directory: `backend`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Environment variables: `DATABASE_URL`, `GEMINI_API_KEY`, `GEMINI_MODEL`

### Frontend

1. New → Web Service → same repo
2. Root directory: `frontend`
3. Build command: `npm install && npm run build`
4. Start command: `npm start`
5. Environment variable: `NEXT_PUBLIC_API_URL=https://chat2sql-backend.onrender.com`

---

## Project Structure

```
chat2sql/
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI app + CORS
│   │   ├── config.py             # Environment variables
│   │   ├── database.py           # SQLAlchemy + schema introspection
│   │   ├── schemas.py            # Pydantic models
│   │   ├── routes/query.py       # POST /query  GET /schemas
│   │   └── services/
│   │       ├── llm_service.py    # Gemini → SQL
│   │       ├── sql_service.py    # Safe SQL execution
│   │       └── chart_service.py  # Chart data transform
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   │   ├── page.tsx              # Main page
│   │   ├── globals.css           # Styles
│   │   └── components/
│   │       ├── ChatBox.tsx       # Query input + results
│   │       ├── SchemaPanel.tsx   # Schema browser sidebar
│   │       ├── ResultsTable.tsx  # Data table
│   │       └── ChartView.tsx     # Bar chart
│   └── lib/api.ts                # API client
├── seed.sql                      # Demo schema + data
├── render.yaml                   # Render deployment config
└── .env.example                  # Environment variable template
```

---

## Security

- Destructive SQL is blocked at the service layer before reaching the database
- Query results are capped at 500 rows
- API keys are environment-variable only — never hardcoded or committed
- CORS configured on the backend

---

## License

MIT
