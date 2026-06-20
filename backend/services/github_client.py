import httpx

from config import GITHUB_API_BASE_URL, get_github_token


def build_github_headers() -> dict[str, str]:
    token = get_github_token()

    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def create_github_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=GITHUB_API_BASE_URL,
        headers=build_github_headers(),
        timeout=httpx.Timeout(30.0),
    )
