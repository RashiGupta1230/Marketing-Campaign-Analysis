"""
AttributeIQ FastAPI Backend — wraps the existing Python analytics engine.
Run: python start.py   OR   uvicorn main:app --reload --port 8000
"""
import sys, os, logging

# Add backend directory and project root to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(backend_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import attribution, optimizer, companies, auth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("attributeiq")

app = FastAPI(
    title="AttributeIQ API",
    description="Marketing Campaign Multi-Touch Attribution & Budget Optimization API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — explicit methods only (no wildcard + credentials)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Company-ID"],
)

app.include_router(auth.router,        prefix="/auth",        tags=["Auth"])
app.include_router(companies.router,   prefix="/companies",   tags=["Companies"])
app.include_router(attribution.router, prefix="/attribution", tags=["Attribution"])
app.include_router(optimizer.router,   prefix="/optimizer",   tags=["Optimizer"])


@app.get("/health", tags=["System"])
async def health():
    return {
        "status": "ok",
        "version": "1.0.0",
        "engine": "Markov Chain + Shapley Value + SciPy SLSQP",
    }


@app.get("/", tags=["System"])
async def root():
    return {"message": "AttributeIQ API", "docs": "/docs", "health": "/health"}
