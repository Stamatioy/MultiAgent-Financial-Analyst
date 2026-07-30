from __future__ import annotations

import json
from typing import TypeVar

from openai import OpenAI
from pydantic import BaseModel, ValidationError

from financial_analyst.config import Settings, get_settings


SchemaT = TypeVar("SchemaT", bound=BaseModel)


class LocalLLMError(RuntimeError):
    """Raised when the local language model cannot produce a valid response."""


class LocalLLMClient:
    """Client for the local llama.cpp OpenAI-compatible server."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

        self.client = OpenAI(
            base_url=self.settings.llm_base_url,
            api_key=self.settings.llm_api_key,
            timeout=self.settings.llm_timeout_seconds,
        )

    def health_check(self) -> bool:
        """Return True when the local model server responds."""

        try:
            models = self.client.models.list()
            return len(models.data) > 0
        except Exception as exc:
            raise LocalLLMError(
                "Could not connect to the local llama.cpp server. "
                "Confirm that llama-server is running on port 8080."
            ) from exc

    def chat(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ) -> str:
        """Generate a normal text response."""

        try:
            response = self.client.chat.completions.create(
                model=self.settings.llm_model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except Exception as exc:
            raise LocalLLMError(
                f"Local model request failed: {exc}"
            ) from exc

        content = response.choices[0].message.content

        if not content:
            raise LocalLLMError("The local model returned an empty response.")

        return content.strip()

    def generate_structured(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[SchemaT],
        temperature: float = 0.1,
        max_tokens: int = 1200,
    ) -> SchemaT:
        """
        Generate JSON and validate it with a Pydantic model.

        We validate application-side even when the server is asked to enforce
        JSON. Model output must never be trusted without validation.
        """

        schema = response_model.model_json_schema()

        try:
            response = self.client.chat.completions.create(
                model=self.settings.llm_model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": response_model.__name__,
                        "schema": schema,
                        "strict": True,
                    },
                },
            )
        except Exception as exc:
            raise LocalLLMError(
                f"Structured local model request failed: {exc}"
            ) from exc

        content = response.choices[0].message.content

        if not content:
            raise LocalLLMError(
                "The local model returned an empty structured response."
            )

        cleaned_content = self._remove_markdown_fences(content)

        try:
            raw_data = json.loads(cleaned_content)
        except json.JSONDecodeError as exc:
            raise LocalLLMError(
                "The model response was not valid JSON.\n\n"
                f"Raw response:\n{content}"
            ) from exc

        try:
            return response_model.model_validate(raw_data)
        except ValidationError as exc:
            raise LocalLLMError(
                "The model returned JSON, but it did not match the schema.\n\n"
                f"Validation error:\n{exc}\n\n"
                f"Raw response:\n{content}"
            ) from exc

    @staticmethod
    def _remove_markdown_fences(content: str) -> str:
        """Remove optional Markdown JSON fences added by a model."""

        stripped = content.strip()

        if stripped.startswith("```json"):
            stripped = stripped[len("```json"):]

        elif stripped.startswith("```"):
            stripped = stripped[len("```"):]

        if stripped.endswith("```"):
            stripped = stripped[:-3]

        return stripped.strip()