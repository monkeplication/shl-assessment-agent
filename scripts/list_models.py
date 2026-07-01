from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

print("Available models:\n")

for model in client.models.list():
    # Only models that support text generation
    if "generateContent" in model.supported_actions:
        print(model.name)