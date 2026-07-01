from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))


from app.catalog import (
    get_all_assessments,
    get_assessment_by_name,
    get_statistics,
)

print(get_statistics())

catalog = get_all_assessments()

print(f"\nLoaded {len(catalog)} assessments")

assessment = get_assessment_by_name("Core Java (Advanced Level) (New)")

print("\nLookup:")

print(assessment)