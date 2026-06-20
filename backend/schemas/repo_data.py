from typing import Optional

from pydantic import BaseModel, Field


class RepoWithReadme(BaseModel):
    """One repository with README content fetched from GitHub (Phase 2 — no AI yet)."""

    repo_name: str
    full_name: str
    html_url: str
    description: Optional[str] = None
    language: Optional[str] = None
    stargazers_count: int
    updated_at: str
    has_readme: bool
    readme_text: Optional[str] = None


class CandidateReposResponse(BaseModel):
    """Full Phase 2 response for a GitHub candidate lookup."""

    username: str = Field(..., description="Normalized GitHub username")
    profile_url: str
    public_repos: int = Field(..., description="Total public repos on the profile")
    repos_analyzed: int = Field(
        ..., description="Number of repos returned after fork filter + cap"
    )
    repos: list[RepoWithReadme]
