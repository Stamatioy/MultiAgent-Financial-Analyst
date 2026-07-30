from __future__ import annotations

import json
from typing import TypeVar

from openai import OpenAI
from pydantic import BaseModel, ValidationError

from financial_analyst.config import Settings, get_settings

import time


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
        max_attempts: int = 2,
    ) -> SchemaT:
        """
        Generate schema-constrained JSON and validate it locally.

        Each retry is a fresh request. We do not feed malformed model output back
        into the prompt because doing so can reinforce incorrect content.
        """

        if max_attempts < 1 or max_attempts > 3:
            raise ValueError("max_attempts must be between 1 and 3.")

        schema = response_model.model_json_schema()
        final_error: Exception | None = None

        for attempt in range(1, max_attempts + 1):
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

                content = response.choices[0].message.content

                if not content:
                    raise LocalLLMError(
                        "The local model returned an empty response."
                    )

                cleaned_content = self._remove_markdown_fences(content)

                raw_data = json.loads(cleaned_content)

                return response_model.model_validate(raw_data)

            except (
                json.JSONDecodeError,
                ValidationError,
                LocalLLMError,
            ) as exc:
                final_error = exc

                if attempt < max_attempts:
                    time.sleep(0.25)
                    continue

            except Exception as exc:
                raise LocalLLMError(
                    f"Structured local model request failed: {exc}"
                ) from exc

        raise LocalLLMError(
            "The local model failed to produce a valid structured response "
            f"after {max_attempts} attempts. Last error: {final_error}"
        ) from final_error

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