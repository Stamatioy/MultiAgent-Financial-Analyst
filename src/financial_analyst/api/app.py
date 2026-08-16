from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware,
)

from financial_analyst.api.routes.health import (
    router as health_router,
)
from financial_analyst.api.routes.research import (
    router as research_router,
)
from financial_analyst.api.routes.research_jobs import (
    router as research_jobs_router,
)
from financial_analyst.api.routes.history import (
    router as history_router,
)
from financial_analyst.api.routes.watchlist import (
    router as watchlist_router,
)
from financial_analyst.api.routes.system import (
    router as system_router,
)

app = FastAPI(
    title="Multi-Agent Financial Analyst API",
    description=(
        "Local multi-agent financial research API."
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

app.include_router(
    research_jobs_router
)

app.include_router(
    health_router
)

app.include_router(
    research_router
)

app.include_router(
    history_router
)
app.include_router(
    watchlist_router
)
app.include_router(
    system_router
)

@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": (
            "Multi-Agent Financial Analyst API"
        ),
        "docs": "/docs",
    }