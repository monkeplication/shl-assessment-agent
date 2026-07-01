from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app.generation import Generator
from app.retrieval import RetrievalEngine
from app.schemas import (
    ExtractionResult,
    Intent,
)


def test_generation():

    retrieval = RetrievalEngine()
    generator = Generator()

    query = "Senior Java backend engineer with Spring Boot and SQL"

    retrieved = retrieval.search(
        query=query,
        top_k=5,
    )

    print("\nRetrieved Results\n")
    print("=" * 70)

    for i, (assessment, score) in enumerate(retrieved, start=1):
        print(f"{i}. {assessment.name}")
        print(f"   Score: {score:.3f}")
        print(f"   Type: {assessment.test_type}")
        print(f"   Duration: {assessment.duration}")
        print()

    assessments = [assessment for assessment, _ in retrieved]

    assert len(assessments) > 0, "No assessments were retrieved!"

    extraction = ExtractionResult(
        role="Backend Engineer",
        seniority="Senior",
        skills=[
            "Java",
            "Spring Boot",
            "SQL",
        ],
    )

    response = generator.generate(
        intent=Intent.RECOMMEND,
        extraction=extraction,
        assessments=assessments,
    )

    print("\n")
    print("=" * 70)
    print("Generated Response")
    print("=" * 70)
    print(response)

    assert isinstance(response, str)
    assert len(response) > 0