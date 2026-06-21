from fastapi import FastAPI, HTTPException
import httpx

from services.exceptions import GitHubUserNotFoundError
from services.github_pipeline import fetch_candidate_repos
from schemas.repo_data import CandidateReposResponse
from schemas.assessment import CandidateAnalysisResponse
from services.analyze_pipeline import analyze_candidate

app = FastAPI(
    title="GitHub Project Assessment API",
    description="Assess a candidate's GitHub project using AI",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/api/repos/{username}", response_model=CandidateReposResponse)
async def get_candidate_repos(username: str):
    try:
        return await fetch_candidate_repos(username)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except GitHubUserNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=f"GitHub user '{exc.username}' not found",
        ) from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail="GitHub API request failed",
        ) from exc


@app.get("/api/analyze/{username}", response_model=CandidateAnalysisResponse)
async def analyze_candidate_repos(username: str):
    try:
        return await analyze_candidate(username)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except GitHubUserNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=f"GitHub user '{exc.username}' not found",
        ) from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail="GitHub API request failed",
        ) from exc
