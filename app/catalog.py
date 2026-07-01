from functools import lru_cache
import json

from app.config import CATALOG_PATH
from app.schemas import Assessment


@lru_cache(maxsize=1)
def load_catalog() -> list[Assessment]:
    """
    Load the SHL catalog into memory.

    The catalog is cached so the JSON file is only
    read once during the application's lifetime.
    """

    with CATALOG_PATH.open("r", encoding="utf-8") as f:
        raw_catalog = json.load(f)

    assessments: list[Assessment] = []

    for item in raw_catalog:
        assessments.append(
            Assessment(
                id=item.get("entity_id"),

                name=item.get("name", "").strip(),
                url=item.get("link", "").strip(),

                description=item.get("description", "").strip(),

                test_type=", ".join(item.get("keys", [])),
                categories=item.get("keys", []),

                duration=item.get("duration", "").strip(),

                remote_testing=item.get("remote", "").lower() == "yes",
                adaptive=item.get("adaptive", "").lower() == "yes",

                job_levels=item.get("job_levels", []),
                languages=item.get("languages", []),

                keywords=item.get("keys", []),
            )
        )

    return assessments


def get_all_assessments() -> list[Assessment]:
    """Return every assessment in the catalog."""
    return load_catalog()


def get_assessment_by_id(entity_id: str) -> Assessment | None:
    """Find an assessment by its SHL entity ID."""

    for assessment in load_catalog():
        if assessment.id == entity_id:
            return assessment

    return None


def get_assessment_by_name(name: str) -> Assessment | None:
    """Find an assessment by its exact name."""

    name = name.lower().strip()

    for assessment in load_catalog():
        if assessment.name.lower() == name:
            return assessment

    return None


def search_assessments(query: str) -> list[Assessment]:
    """
    Temporary keyword search.

    This will later be replaced by semantic vector search.
    """

    query = query.lower().strip()

    results: list[Assessment] = []

    for assessment in load_catalog():

        searchable_text = " ".join(
            [
                assessment.name,
                assessment.description or "",
                assessment.test_type or "",
                " ".join(assessment.categories),
                " ".join(assessment.keywords),
            ]
        ).lower()

        if query in searchable_text:
            results.append(assessment)

    return results


def get_statistics() -> dict:
    """Return basic statistics about the catalog."""

    catalog = load_catalog()

    return {
        "total_assessments": len(catalog),
        "remote_enabled": sum(a.remote_testing for a in catalog),
        "adaptive_assessments": sum(a.adaptive for a in catalog),
        "with_duration": sum(bool(a.duration) for a in catalog),
    }