import asyncio
import base64

import httpx


async def fetch_repo_readme(
    client: httpx.AsyncClient,
    owner: str,
    repo_name: str,
) -> dict:
    """
    Fetch one repo README.

    Returns:
        {
            "readme_text": str | None,
            "has_readme": bool,
        }
    """
    response = await client.get(f"/repos/{owner}/{repo_name}/readme")

    if response.status_code == 404:
        return {
            "readme_text": None,
            "has_readme": False,
        }

    response.raise_for_status()
    data = response.json()

    encoded_content = data["content"]
    readme_bytes = base64.b64decode(encoded_content)
    readme_text = readme_bytes.decode("utf-8", errors="replace")

    return {
        "readme_text": readme_text,
        "has_readme": True,
    }


async def fetch_readmes_for_repos(
    client: httpx.AsyncClient,
    username: str,
    repos: list[dict],
) -> list[dict]:
    """
    Fetch READMEs for multiple repos concurrently.
    """

    async def fetch_one(repo: dict) -> dict:
        readme_data = await fetch_repo_readme(client, username, repo["name"])
        return {
            **repo,
            "readme_text": readme_data["readme_text"],
            "has_readme": readme_data["has_readme"],
        }

    tasks = [fetch_one(repo) for repo in repos]
    return list(await asyncio.gather(*tasks))
