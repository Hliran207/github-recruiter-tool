from config import MAX_REPOS_TO_ANALYZE
from schemas.repo_data import CandidateReposResponse, RepoWithReadme
from services.github_client import create_github_client
from services.github_readme import fetch_readmes_for_repos
from services.github_repos import fetch_user_repos
from services.github_user import fetch_github_user
from utils.github_input import normalize_github_username
from utils.repo_filters import cap_repo_count, exclude_forks


async def fetch_candidate_repos(raw_username: str) -> CandidateReposResponse:
    username = normalize_github_username(raw_username)

    async with create_github_client() as client:
        user = await fetch_github_user(client, username)

        repos = await fetch_user_repos(client, username)
        repos = exclude_forks(repos)
        repos = cap_repo_count(repos, MAX_REPOS_TO_ANALYZE)

        enriched_repos = await fetch_readmes_for_repos(client, username, repos)

    repo_models = [
        RepoWithReadme(
            repo_name=repo["name"],
            full_name=repo["full_name"],
            html_url=repo["html_url"],
            description=repo.get("description"),
            language=repo.get("language"),
            stargazers_count=repo["stargazers_count"],
            updated_at=repo["updated_at"],
            has_readme=repo["has_readme"],
            readme_text=repo["readme_text"],
        )
        for repo in enriched_repos
    ]

    return CandidateReposResponse(
        username=user["login"],
        profile_url=user["html_url"],
        public_repos=user["public_repos"],
        repos_analyzed=len(repo_models),
        repos=repo_models,
    )
