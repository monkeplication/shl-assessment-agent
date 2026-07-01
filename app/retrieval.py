from pathlib import Path
import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.schemas import Assessment

INDEX_DIR = Path("data/catalog_index")
MODEL_NAME = "all-MiniLM-L6-v2"

# Tune this later after testing the traces
SIMILARITY_THRESHOLD = 0.35


class RetrievalEngine:
    """
    Semantic retrieval engine for SHL assessments.
    """

    def __init__(self):
        print("Loading embedding model...")

        self.model = SentenceTransformer(MODEL_NAME)

        print("Loading FAISS index...")

        self.index = faiss.read_index(
            str(INDEX_DIR / "catalog.faiss")
        )

        print("Loading catalog metadata...")

        with open(
            INDEX_DIR / "catalog_metadata.json",
            "r",
            encoding="utf-8",
        ) as f:
            metadata = json.load(f)

        self.assessments: list[Assessment] = []

        for item in metadata:
            self.assessments.append(
                Assessment(
                    id=item.get("entity_id"),

                    name=item.get("name"),
                    url=item.get("link"),

                    description=item.get("description"),

                    test_type=", ".join(item.get("keys", [])),
                    categories=item.get("keys", []),

                    duration=item.get("duration"),

                    remote_testing=item.get("remote", "").lower() == "yes",
                    adaptive=item.get("adaptive", "").lower() == "yes",

                    job_levels=item.get("job_levels", []),
                    languages=item.get("languages", []),

                    keywords=item.get("keys", []),
                )
            )

        print(f"Loaded {len(self.assessments)} assessments.\n")

    def embed_query(self, query: str) -> np.ndarray:
        """
        Convert a user query into an embedding.
        """

        embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding.astype(np.float32)

    def search(
        self,
        query: str,
        top_k: int = 10,
        min_score: float = SIMILARITY_THRESHOLD,
    ) -> list[tuple[Assessment, float]]:
        """
        Perform semantic search.

        Returns:
            List of (Assessment, Similarity Score)
        """

        query_embedding = self.embed_query(query)

        scores, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            if score < min_score:
                continue

            results.append(
                (
                    self.assessments[idx],
                    float(score),
                )
            )

        return results