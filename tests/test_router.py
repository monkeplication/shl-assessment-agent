from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app.router import Router
from app.schemas import ExtractionResult

router = Router()

cases = [

    (
        "Recommend",
        ExtractionResult(
            role="Backend Engineer",
            skills=["Java"],
        )
    ),

    (
        "Clarify",
        ExtractionResult()
    ),

    (
        "Refine",
        ExtractionResult(
            refinement="shorter duration"
        )
    ),

    (
        "Compare",
        ExtractionResult(
            compare_items=[
                "Java",
                "Python"
            ]
        )
    ),

    (
        "Refuse",
        ExtractionResult(
            prompt_injection=True
        )
    )

]

for name, extraction in cases:

    result = router.route(extraction)

    print(name, "->", result.value)