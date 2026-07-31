from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer

from financial_analyst.config import get_settings


class EmbeddingService:
    """Local sentence-transformer embedding model."""

    def __init__(
        self,
        model_name: str | None = None,
    ) -> None:
        settings = get_settings()

        self.model_name = (
            model_name
            or settings.embedding_model
        )

        self.model = SentenceTransformer(
            self.model_name,
            device="cpu",
        )

    @property
    def dimension(self) -> int:
        dimension = (
            self.model.get_sentence_embedding_dimension()
        )

        if dimension is None:
            raise RuntimeError(
                "Embedding model did not report its dimension."
            )

        return int(dimension)

    def encode(
        self,
        texts: list[str],
    ) -> np.ndarray:
        if not texts:
            return np.empty(
                (0, self.dimension),
                dtype=np.float32,
            )

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return np.asarray(
            embeddings,
            dtype=np.float32,
        )

    def encode_query(
        self,
        query: str,
    ) -> np.ndarray:
        text = query.strip()

        if not text:
            raise ValueError(
                "Retrieval query cannot be empty."
            )

        return self.encode([text])