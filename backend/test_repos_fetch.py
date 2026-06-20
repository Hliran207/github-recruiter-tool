import asyncio

from config import MAX_REPOS_TO_ANALYZE
from services.github_client import create_github_client
from services.github_repos import fetch_user_repos
from services.github_user import fetch_github_user
from utils.github_input import normalize_github_username
from utils.repo_filters import cap_repo_count, exclude_forks


async def main():
    async with create_github_client() as client:
        username = normalize_github_username("torvalds")
        await fetch_github_user(client, username)

        all_repos = await fetch_user_repos(client, username)
        original_repos = exclude_forks(all_repos)
        capped_repos = cap_repo_count(original_repos, MAX_REPOS_TO_ANALYZE)

        print("fetched from GitHub:", len(all_repos))
        print("after excluding forks:", len(original_repos))
        print(f"after cap ({MAX_REPOS_TO_ANALYZE}):", len(capped_repos))

        print("\nRepos we will analyze:")
        for repo in capped_repos:
            print("-", repo["name"], "| updated:", repo["updated_at"])


asyncio.run(main())
