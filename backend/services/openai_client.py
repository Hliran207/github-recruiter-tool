from openai import AsyncOpenAI

from config import OPENAI_REQUEST_TIMEOUT_SECONDS, get_openai_api_key

_client: AsyncOpenAI | None = None


def get_openai_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(
            api_key=get_openai_api_key(),
            timeout=OPENAI_REQUEST_TIMEOUT_SECONDS,
        )
    return _client
