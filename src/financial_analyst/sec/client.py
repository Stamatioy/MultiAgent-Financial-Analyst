from __future__ import annotations

import time
from typing import Any

import httpx

from financial_analyst.config import Settings, get_settings


class SECClientError(RuntimeError):
    """Raised when an SEC request fails."""


class SECClient:
    """Minimal client for data.sec.gov."""

    def __init__(
        self,
        settings: Settings | None = None,
    ) -> None:
        self.settings = settings or get_settings()

        self.client = httpx.Client(
            base_url=self.settings.sec_base_url,
            headers={
                "User-Agent": self.settings.sec_user_agent,
                "Accept-Encoding": "gzip, deflate",
                "Accept": "application/json",
            },
            timeout=30.0,
        )

        self._last_request_time = 0.0

    def get_json(
        self,
        path: str,
    ) -> dict[str, Any]:
        self._rate_limit()

        try:
            response = self.client.get(path)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise SECClientError(
                f"SEC request failed for {path}: {exc}"
            ) from exc

        try:
            return response.json()
        except ValueError as exc:
            raise SECClientError(
                f"SEC returned invalid JSON for {path}."
            ) from exc

    def _rate_limit(self) -> None:
        """
        Keep requests comfortably below SEC's fair-access ceiling.

        0.15 seconds between requests ≈ max 6.7 requests/sec.
        """

        minimum_interval = 0.15

        elapsed = time.monotonic() - self._last_request_time

        if elapsed < minimum_interval:
            time.sleep(minimum_interval - elapsed)

        self._last_request_time = time.monotonic()

    def get_absolute_json(
        self,
        url: str,
    ) -> dict[str, Any]:
        self._rate_limit()

        try:
            response = self.client.get(url)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise SECClientError(
                f"SEC request failed for {url}: {exc}"
            ) from exc

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> "SECClient":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()