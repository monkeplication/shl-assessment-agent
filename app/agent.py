from app.decision import should_recommend
from app.extraction import Extractor
from app.generation import Generator
from app.retrieval import RetrievalEngine
from app.router import Router
from app.schemas import (
    ChatRequest,
    ChatResponse,
    Recommendation,
    Intent,
)


class AssessmentAgent:

    def __init__(self):

        self.extractor = Extractor()
        self.router = Router()
        self.retrieval = RetrievalEngine()
        self.generator = Generator()

    def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:

        # 1. Understand the conversation
        extraction = self.extractor.extract(request)
        print("=" * 60)
        print("EXTRACTION")
        print(extraction.model_dump())
        print("=" * 60)

        # 2. Decide whether we need more information
        ready, question = should_recommend(extraction)

        if not ready:
            return ChatResponse(
                reply=question,
                recommendations=None,
                end_of_conversation=False,
            )

        # 3. Determine intent
        intent = self.router.route(extraction)

        # 4. Retrieve assessments if needed
        assessments = []

        if intent in (
            Intent.RECOMMEND,
            Intent.COMPARE,
            Intent.REFINE,
        ):

            query = " ".join(
                [
                    extraction.role or "",
                    extraction.seniority or "",
                    *extraction.skills,
                ]
            )

            results = self.retrieval.search(
                query=query,
                top_k=5,
            )

            assessments = [
                assessment
                for assessment, _ in results
            ]

        # 5. Generate response
        reply = self.generator.generate(
            intent=intent,
            extraction=extraction,
            assessments=assessments,
        )

        # 6. Convert to API response
        recommendations = [
            Recommendation(
                name=a.name,
                url=a.url,
                test_type=a.test_type,
            )
            for a in assessments
        ]

        return ChatResponse(
            reply=question,
            recommendations=None,
            end_of_conversation=False,
)