import json
from pathlib import Path

catalog_path = Path("data/catalog.json")

try:
    with catalog_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    print("✅ JSON loaded successfully!")
    print(f"Total assessments: {len(data)}")

    print("\nFirst assessment:")
    print(data[0]["name"])

except Exception as e:
    print("❌ Failed to load JSON")
    print(type(e).__name__)
    print(e)