import asyncio

from schemas.assessment import RepoAssessment
from services.assessment_service import assess_repo_with_llm


async def main():
    # repo = {
    #     "repo_name": "demo-api",
    #     "description": "A small REST API for learning FastAPI",
    #     "language": "Python",
    #     "stargazers_count": 2,
    #     "updated_at": "2024-08-15T10:00:00Z",
    #     "has_readme": True,
    #     "readme_text": (
    #         "# Demo API\n\n"
    #         "A learning project with CRUD endpoints for tasks.\n\n"
    #         "## Setup\n"
    #         "1. pip install -r requirements.txt\n"
    #         "2. uvicorn main:app --reload\n"
    #     ),
    # }

    # llm_result = await assess_repo_with_llm(repo)

    # full = RepoAssessment(
    #     repo_name=repo["repo_name"],
    #     has_readme=repo["has_readme"],
    #     **llm_result.model_dump(),
    # )

    # print(full.model_dump())
    without_readme = {
        "repo_name": "empty-repo",
        "description": "Has a GitHub one-liner but no README file",
        "language": "JavaScript",
        "stargazers_count": 0,
        "updated_at": "2023-01-01T00:00:00Z",
        "has_readme": False,
        "readme_text": None,
    }
    print(without_readme)


asyncio.run(main())
