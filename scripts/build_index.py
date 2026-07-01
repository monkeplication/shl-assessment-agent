from pathlib import Path
import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

CATALOG_PATH = Path("data/catalog.json")
INDEX_DIR = Path("data/catalog_index")

MODEL_NAME = "all-MiniLM-L6-v2"


def load_catalog():
    with CATALOG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_document(item: dict) -> str:
    """
    Convert one assessment into searchable text.
    """

    return "\n".join(
        [
            item.get("name", ""),
            item.get("description", ""),
            " ".join(item.get("keys", [])),
            " ".join(item.get("job_levels", [])),
            " ".join(item.get("languages", [])),
        ]
    )


def main():

    print("Loading catalog...")

    catalog = load_catalog()

    print(f"{len(catalog)} assessments loaded.")

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    documents = [
        build_document(item)
        for item in catalog
    ]

    print("Generating embeddings...")

    embeddings = model.encode(
        documents,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings.astype(np.float32))

    INDEX_DIR.mkdir(exist_ok=True)

    faiss.write_index(
        index,
        str(INDEX_DIR / "catalog.faiss"),
    )

    with open(
        INDEX_DIR / "catalog_metadata.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            catalog,
            f,
            indent=2,
        )

    print("\nDone!")

    print(f"Vectors : {index.ntotal}")

    print(f"Dimension : {dimension}")
    print(f"Saved to {INDEX_DIR}")


if __name__ == "__main__":
    main()