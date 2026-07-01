from fastapi import FastAPI

from app.agent import AssessmentAgent
from app.schemas import ChatRequest

app = FastAPI(
    title="SHL Assessment Recommendation Agent",
    version="1.0.0",
)

agent = AssessmentAgent()


@app.get("/")
def root():
    return {
        "message": "SHL Assessment Recommendation Agent"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    return agent.chat(request)