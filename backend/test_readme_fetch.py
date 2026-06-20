import asyncio

from config import MAX_REPOS_TO_ANALYZE
from services.github_client import create_github_client
from services.github_readme import fetch_readmes_for_repos
from services.github_repos import fetch_user_repos
from services.github_user import fetch_github_user
from utils.github_input import normalize_github_username
from utils.repo_filters import cap_repo_count, exclude_forks


async def main():
    async with create_github_client() as client:
        username = normalize_github_username("torvalds")
        await fetch_github_user(client, username)

        repos = await fetch_user_repos(client, username)
        repos = exclude_forks(repos)
        repos = cap_repo_count(repos, MAX_REPOS_TO_ANALYZE)

        enriched = await fetch_readmes_for_repos(client, username, repos)

        for repo in enriched:
            preview = (repo["readme_text"] or "")[:80].replace("\n", " ")
            print(
                repo["name"],
                "| has_readme:",
                repo["has_readme"],
                "| preview:",
                preview or "(none)",
            )


asyncio.run(main())
