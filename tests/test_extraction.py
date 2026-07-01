from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app.extraction import Extractor
from app.schemas import ChatRequest, Message

extractor = Extractor()

request = ChatRequest(
    messages=[
        Message(
            role="user",
            content=(
                "I'm hiring a senior backend engineer. "
                "Need Java, Spring Boot, SQL and AWS."
            ),
        )
    ]
)

result = extractor.extract(request)

print(result.model_dump_json(indent=4))