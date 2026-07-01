from app.llm_client import LLMClient
from app.prompts import EXTRACTION_PROMPT
from app.schemas import (
    ChatRequest,
    ExtractionResult,
)


VALID_INTENTS = {
    "clarify",
    "recommend",
    "refine",
    "compare",
    "refuse",
    "end",
}


class Extractor:

    def __init__(self):
        self.llm = LLMClient()

    def extract(
        self,
        request: ChatRequest,
    ) -> ExtractionResult:

        conversation = "\n".join(
            f"{message.role.upper()}: {message.content}"
            for message in request.messages
        )

        data = self.llm.generate_json(
            system_prompt=EXTRACTION_PROMPT,
            user_prompt=conversation,
            temperature=0.0,
        )

        # ---------- Defaults ----------

        data.setdefault("role", None)
        data.setdefault("industry", None)
        data.setdefault("seniority", None)
        data.setdefault("experience_years", None)

        data.setdefault("skills", [])

        data.setdefault("language", None)
        data.setdefault("location", None)

        data.setdefault("volume_hiring", None)

        data.setdefault("wants_personality", None)
        data.setdefault("wants_cognitive", None)
        data.setdefault("wants_simulation", None)
        data.setdefault("wants_knowledge", None)

        data.setdefault("compare_items", [])

        data.setdefault("refinement", None)

        data.setdefault("legal_question", False)
        data.setdefault("off_topic", False)
        data.setdefault("prompt_injection", False)

        data.setdefault("intent", "recommend")

        # ---------- Fix None values ----------

        if data["skills"] is None:
            data["skills"] = []

        if data["compare_items"] is None:
            data["compare_items"] = []

        for field in (
            "legal_question",
            "off_topic",
            "prompt_injection",
        ):
            if data[field] is None:
                data[field] = False

        # ---------- Rule-based corrections ----------

        conversation_lower = conversation.lower()

        # Selection / Hiring
        if any(
            word in conversation_lower
            for word in (
                "selection",
                "hire",
                "hiring",
                "recruit",
                "recruitment",
                "screening",
                "candidate",
            )
        ):
            data["refinement"] = "selection"

        # Development
        if any(
            word in conversation_lower
            for word in (
                "development",
                "coach",
                "coaching",
                "promotion",
                "succession",
                "developmental",
            )
        ):
            data["refinement"] = "development"

        # Leadership personality assessments
        if any(
            word in conversation_lower
            for word in (
                "leadership",
                "leader",
                "executive",
                "director",
                "cxo",
                "manager",
            )
        ):
            if data["wants_personality"] is None:
                data["wants_personality"] = True

        # Volume hiring
        if any(
            word in conversation_lower
            for word in (
                "bulk",
                "mass hiring",
                "volume hiring",
                "campus",
                "graduate hiring",
            )
        ):
            data["volume_hiring"] = True

        # ---------- Normalize intent ----------

        if data["intent"] not in VALID_INTENTS:
            data["intent"] = "recommend"

        return ExtractionResult.model_validate(data)