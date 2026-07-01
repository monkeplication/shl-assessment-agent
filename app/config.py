from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

CATALOG_PATH = DATA_DIR / "catalog.json"

INDEX_DIR = DATA_DIR / "catalog_index"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "models/gemini-flash-lite-latest"