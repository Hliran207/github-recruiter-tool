import httpx

from config import GITHUB_API_BASE_URL, get_github_token


def build_github_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = get_github_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def create_github_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=GITHUB_API_BASE_URL,
        headers=build_github_headers(),
        timeout=httpx.Timeout(30.0),
    )
