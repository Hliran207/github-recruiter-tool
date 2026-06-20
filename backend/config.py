import os
from pathlib import Path

from dotenv import load_dotenv

# Load backend/.env when this module is imported
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)

GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_github_token() -> str:
    token = GITHUB_TOKEN
    if not token:
        raise RuntimeError(
            "GITHUB_TOKEN is not set. Add it to backend/.env (see .env.example)."
        )
    return token


MAX_REPOS_TO_ANALYZE = 10
