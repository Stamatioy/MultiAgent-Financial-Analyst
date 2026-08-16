from __future__ import annotations

import os

import httpx

from fastapi import APIRouter


router = APIRouter(
    prefix="/api/system",
    tags=["system"],
)


LLAMA_CPP_URL = (
    os.getenv(
        "LLAMA_CPP_URL",
        "http://127.0.0.1:8080",
    )
    .rstrip("/")
)


@router.get("/status")
def get_system_status() -> dict:
    llama_online = False

    try:
        response = httpx.get(
            f"{LLAMA_CPP_URL}/health",
            timeout=2.0,
        )

        llama_online = (
            response.status_code
            < 500
        )

    except httpx.HTTPError:
        llama_online = False

    return {
        "api": {
            "online": True,
        },

        "llm": {
            "online": llama_online,
            "model": "Qwen3-8B",
            "runtime": "llama.cpp",
            "local": True,
        },
    }