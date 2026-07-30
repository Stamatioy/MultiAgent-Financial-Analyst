from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Application configuration loaded from environment variables."""

    llm_base_url: str
    llm_api_key: str
    llm_model: str
    llm_timeout_seconds: float
    market_database_path: Path


def get_settings() -> Settings:
    """Load and validate application settings."""

    base_url = os.getenv("LLM_BASE_URL")
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL")

    if not base_url:
        raise RuntimeError("LLM_BASE_URL is missing from the environment.")

    if not api_key:
        raise RuntimeError("LLM_API_KEY is missing from the environment.")

    if not model:
        raise RuntimeError("LLM_MODEL is missing from the environment.")

    timeout_text = os.getenv("LLM_TIMEOUT_SECONDS", "180")

    try:
        timeout_seconds = float(timeout_text)
    except ValueError as exc:
        raise RuntimeError(
            "LLM_TIMEOUT_SECONDS must be a valid number."
        ) from exc

    database_path = Path(
        os.getenv("MARKET_DATABASE_PATH", "data/market.duckdb")
    )

    return Settings(
        llm_base_url=base_url.rstrip("/"),
        llm_api_key=api_key,
        llm_model=model,
        llm_timeout_seconds=timeout_seconds,
        market_database_path=database_path,
    )