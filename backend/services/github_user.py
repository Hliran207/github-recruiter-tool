import httpx
from services.exceptions import GitHubUserNotFoundError


async def fetch_github_user(
    client: httpx.AsyncClient,
    username: str,
) -> dict:
    """
    Verify that a GitHub user exists and return basic public profile metadata.
    Raises:
        GitHubUserNotFoundError: if the user does not exist (HTTP 404).
        httpx.HTTPStatusError: for other unexpected HTTP errors (401, 403, 5xx).
    """
    response = await client.get(f"/users/{username}")
    if response.status_code == 404:
        raise GitHubUserNotFoundError(username)
    response.raise_for_status()
    data = response.json()
    return {
        "login": data["login"],
        "html_url": data["html_url"],
        "public_repos": data["public_repos"],
        "name": data.get("name"),
        "bio": data.get("bio"),
    }
