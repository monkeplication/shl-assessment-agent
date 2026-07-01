from app.schemas import (
    ExtractionResult,
    Intent,
)


class Router:
    """
    Determines what the agent should do next
    based on the extracted info
    """

    def route(
        self,
        extraction: ExtractionResult,
    ) -> Intent:

        # ---------- Safety ----------
        if extraction.prompt_injection:
            return Intent.REFUSE

        if extraction.off_topic:
            return Intent.REFUSE

        if extraction.legal_question:
            return Intent.REFUSE

        # ---------- Compare ----------
        if len(extraction.compare_items) >= 2:
            return Intent.COMPARE

        # ---------- Refinement ----------
        if extraction.refinement:
            return Intent.REFINE

        # ---------- Missing information ----------
        if extraction.role is None and len(extraction.skills) == 0:
            return Intent.CLARIFY

        # ---------- Recommendation ----------
        return Intent.RECOMMEND