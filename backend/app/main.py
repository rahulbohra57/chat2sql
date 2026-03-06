from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import query

app = FastAPI(title="AI SQL Analyst", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router)


@app.get("/")
def home():
    return {"message": "AI SQL Analyst API"}
