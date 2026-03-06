# Chat2SQL — AI SQL Analyst

* **Live App:** [https://chat2sql-frontend.onrender.com](https://chat2sql-frontend.onrender.com)
* **API:** [https://chat2sql-ctjb.onrender.com](https://chat2sql-ctjb.onrender.com)
* **For testing:**
  - id: admin
  - password: admin@123

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

<img width="1536" height="1024" alt="chat2sql" src="https://github.com/user-attachments/assets/a83f4e5e-cd2c-4870-a914-4d59bbd2befd" />

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
