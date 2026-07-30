from __future__ import annotations

from typing import Protocol, TypeVar


InputT = TypeVar("InputT", contravariant=True)
OutputT = TypeVar("OutputT", covariant=True)


class Agent(Protocol[InputT, OutputT]):
    """Minimal interface implemented by deterministic agent wrappers."""

    def analyze(self, value: InputT) -> OutputT:
        ...