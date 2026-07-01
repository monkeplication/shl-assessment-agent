from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app.retrieval import RetrievalEngine

engine = RetrievalEngine()

query = "Senior Java backend engineer with Spring Boot and SQL"

results = engine.search(
    query=query,
    top_k=10,
)

print(f"\nQuery: {query}\n")

for i, (assessment, score) in enumerate(results, start=1):

    print("=" * 70)

    print(f"Rank : {i}")
    print(f"Score: {score:.3f}")

    print(f"Name : {assessment.name}")

    print(f"Type : {assessment.test_type}")

    print(f"Duration : {assessment.duration}")

    print(f"URL : {assessment.url}")