import os
from pathlib import Path

from dotenv import load_dotenv

# Load backend/.env when this module is imported
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)

MAX_REPOS_TO_ANALYZE = 10

# Maximum number of characters in a README to analyze - Just Safety guardrail for README size
MAX_README_CHARS = 15_000

# Timeout for OpenAI API requests
OPENAI_REQUEST_TIMEOUT_SECONDS = 60.0


GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_github_token() -> str:
    token = GITHUB_TOKEN
    if not token:
        raise RuntimeError(
            "GITHUB_TOKEN is not set. Add it to backend/.env (see .env.example)."
        )
    return token


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_TEMPERATURE = 0.2


def get_openai_api_key() -> str:
    api_key = OPENAI_API_KEY
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to backend/.env (see .env.example)."
        )
    return api_key
