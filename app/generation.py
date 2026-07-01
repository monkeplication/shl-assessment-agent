from app.llm_client import LLMClient
from app.prompts import (
    RECOMMEND_PROMPT,
    COMPARE_PROMPT,
)
from app.schemas import (
    Assessment,
    ExtractionResult,
    Intent,
)


class Generator:

    def __init__(self):
        self.llm = LLMClient()

    def generate(
        self,
        intent: Intent,
        extraction: ExtractionResult,
        assessments: list[Assessment],
    ) -> str:

        if intent == Intent.CLARIFY:
            return self._clarify(extraction)

        if intent == Intent.REFUSE:
            return self._refuse()

        if intent == Intent.RECOMMEND:
            return self._recommend(
                extraction,
                assessments,
            )

        if intent == Intent.COMPARE:
            return self._compare(
                assessments,
            )

        if intent == Intent.REFINE:
            return self._recommend(
                extraction,
                assessments,
            )

        return "I'm not sure how to help with that."

    def _clarify(
        self,
        extraction: ExtractionResult,
    ) -> str:

        return (
            "Could you tell me the role or the main skills "
            "you're hiring for?"
        )

    def _refuse(self) -> str:

        return (
            "I can only help with SHL assessment recommendations."
        )

    def _recommend(
        self,
        extraction: ExtractionResult,
        assessments: list[Assessment],
    ) -> str:

        context = ""

        for assessment in assessments:

            context += f"""
Name: {assessment.name}
Type: {assessment.test_type}
Duration: {assessment.duration}
Description: {assessment.description}

"""

        user_info = extraction.model_dump_json(indent=2)

        return self.llm.generate(
            system_prompt=RECOMMEND_PROMPT,
            user_prompt=f"""
User Requirements

{user_info}

Candidate Assessments

{context}
""",
        )

    def _compare(
        self,
        assessments: list[Assessment],
    ) -> str:

        context = ""

        for assessment in assessments:

            context += f"""
Name: {assessment.name}
Description: {assessment.description}
Duration: {assessment.duration}
"""

        return self.llm.generate(
            system_prompt=COMPARE_PROMPT,
            user_prompt=context,
        )