import httpx


async def fetch_user_repos(client: httpx.AsyncClient, username: str) -> list[dict]:
    """
    Fetch public repos for Github user (first page, sorted by updated)
    """

    response = await client.get(
        f"/users/{username}/repos",
        params={
            "per_page": 100,
            "sort": "updated",
            "direction": "desc",
            "type": "owner",
        },
    )

    response.raise_for_status()
    repos_json = response.json()

    return [
        {
            "name": repo["name"],
            "full_name": repo["full_name"],
            "html_url": repo["html_url"],
            "description": repo.get("description"),
            "fork": repo["fork"],
            "language": repo.get("language"),
            "stargazers_count": repo["stargazers_count"],
            "updated_at": repo["updated_at"],
            "default_branch": repo.get("default_branch"),
        }
        for repo in repos_json
    ]
