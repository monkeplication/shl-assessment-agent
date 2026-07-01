from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY, MODEL_NAME


class LLMClient:
    """
    Thin wrapper around the Gemini API.
    """

    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found in .env"
            )

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ) -> str:
        """
        Generate normal text.
        """

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                system_prompt,
                user_prompt,
            ],
            config=types.GenerateContentConfig(
                temperature=temperature,
            ),
        )

        return response.text.strip()

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
    ) -> dict:
        """
        Generate structured JSON.
        """

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                system_prompt,
                user_prompt,
            ],
            config=types.GenerateContentConfig(
                temperature=temperature,
                response_mime_type="application/json",
            ),
        )

        if hasattr(response, "parsed") and response.parsed:
            return response.parsed

        import json

        return json.loads(response.text)