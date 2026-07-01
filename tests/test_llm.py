from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app.llm_client import LLMClient

llm = LLMClient()

response = llm.generate(
    system_prompt="You are a helpful assistant.",
    user_prompt="Reply with exactly: Hello World"
)

print(response)