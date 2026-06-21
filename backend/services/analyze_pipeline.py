from schemas.assessment import CandidateAnalysisResponse
from services.assessment_service import assess_repos_batch
from services.github_pipeline import fetch_candidate_repos


def _repo_to_assessment_input(repo) -> dict:
    """
    Normalize Phase 2 repo shape for assessment_service.
    Works with RepoWithReadme models or equivalent dicts.
    """
    if hasattr(repo, "model_dump"):
        data = repo.model_dump()
    else:
        data = repo

    return {
        "repo_name": data["repo_name"],
        "description": data.get("description"),
        "language": data.get("language"),
        "stargazers_count": data.get("stargazers_count", 0),
        "updated_at": data.get("updated_at", ""),
        "has_readme": data.get("has_readme", False),
        "readme_text": data.get("readme_text"),
    }


async def analyze_candidate(raw_username: str) -> CandidateAnalysisResponse:
    """
    Full pipeline:
      normalize + GitHub fetch (Phase 2)
      → concurrent AI assessment (Phase 3)
    """
    candidate_data = await fetch_candidate_repos(raw_username)

    repo_inputs = [_repo_to_assessment_input(repo) for repo in candidate_data.repos]
    assessments = await assess_repos_batch(repo_inputs)

    return CandidateAnalysisResponse(
        username=candidate_data.username,
        profile_url=candidate_data.profile_url,
        public_repos=candidate_data.public_repos,
        repos_analyzed=candidate_data.repos_analyzed,
        assessments=assessments,
    )
