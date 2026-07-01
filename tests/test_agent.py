from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app.agent import AssessmentAgent
from app.schemas import ChatRequest, Message


def test_agent():

    agent = AssessmentAgent()

    request = ChatRequest(
        messages=[
            Message(
                role="user",
                content=(
                    "I need an assessment for a Senior "
                    "Backend Engineer with Java, Spring Boot, "
                    "SQL and AWS."
                ),
            )
        ]
    )

    response = agent.chat(request)

    print("\nReply\n")
    print(response.reply)

    print("\nRecommendations\n")

    for recommendation in response.recommendations:
        print(recommendation.name)

    assert len(response.reply) > 0