from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


# ==========================
# API MODELS
# ==========================

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str


class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation]
    end_of_conversation: bool


# ==========================
# INTERNAL MODELS
# ==========================

class Intent(str, Enum):
    CLARIFY = "clarify"
    RECOMMEND = "recommend"
    REFINE = "refine"
    COMPARE = "compare"
    REFUSE = "refuse"
    END = "end"


class Assessment(BaseModel):
    id: Optional[str] = None

    name: str
    url: str

    description: Optional[str] = None

    test_type: Optional[str] = None
    categories: List[str] = Field(default_factory=list)

    duration: Optional[str] = None

    remote_testing: bool = False
    adaptive: bool = False

    job_levels: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)

    keywords: List[str] = Field(default_factory=list)


class ExtractionResult(BaseModel):
    role: Optional[str] = None
    industry: Optional[str] = None
    seniority: Optional[str] = None
    experience_years: Optional[int] = None

    skills: List[str] = Field(default_factory=list)

    language: Optional[str] = None
    location: Optional[str] = None

    volume_hiring: Optional[bool] = None

    wants_personality: Optional[bool] = None
    wants_cognitive: Optional[bool] = None
    wants_simulation: Optional[bool] = None
    wants_knowledge: Optional[bool] = None

    compare_items: List[str] = Field(default_factory=list)

    refinement: Optional[str] = None

    legal_question: bool = False
    off_topic: bool = False
    prompt_injection: bool = False

    intent: Optional[Intent] = None


class ConversationState(BaseModel):
    extraction: ExtractionResult

    recommendations: List[Assessment] = Field(default_factory=list)

    turn_count: int = 0

    conversation_complete: bool = False