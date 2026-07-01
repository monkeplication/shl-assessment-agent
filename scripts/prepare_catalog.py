import json
from pathlib import Path
from collections import Counter

CATALOG_PATH = Path("data/catalog.json")


def load_catalog():
    with CATALOG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_assessment(item):
    return {
        "id": item.get("entity_id"),
        "name": item.get("name", "").strip(),
        "url": item.get("link", "").strip(),
        "description": item.get("description", "").strip(),
        "duration": item.get("duration", "").strip(),
        "remote_testing": item.get("remote", "").lower() == "yes",
        "adaptive": item.get("adaptive", "").lower() == "yes",
        "job_levels": item.get("job_levels", []),
        "languages": item.get("languages", []),
        "categories": item.get("keys", []),
    }


def main():
    raw_catalog = load_catalog()

    catalog = [normalize_assessment(item) for item in raw_catalog]

    print("=" * 50)
    print("SHL Catalog Statistics")
    print("=" * 50)

    print(f"Total Assessments : {len(catalog)}")

    missing_description = sum(
        not item["description"] for item in catalog
    )

    missing_duration = sum(
        not item["duration"] for item in catalog
    )

    print(f"Missing Description : {missing_description}")
    print(f"Missing Duration    : {missing_duration}")

    categories = Counter()

    for item in catalog:
        categories.update(item["categories"])

    print("\nTop Categories")

    for category, count in categories.most_common():
        print(f"{category:35} {count}")


if __name__ == "__main__":
    main()