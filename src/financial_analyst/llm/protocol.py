from __future__ import annotations

from typing import Protocol, TypeVar

from pydantic import BaseModel


SchemaT = TypeVar("SchemaT", bound=BaseModel)


class StructuredLLMClient(Protocol):
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
        ...