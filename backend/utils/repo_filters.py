def exclude_forks(repos: list[dict]) -> list[dict]:
    """Return only non-fork repositories."""
    return [repo for repo in repos if not repo["fork"]]


def cap_repo_count(repos: list[dict], limit: int) -> list[dict]:
    """Keep only the first `limit` repos (caller should already have sorted/filtered)."""
    return repos[:limit]
