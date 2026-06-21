import asyncio

from openai import APIConnectionError, APIStatusError, RateLimitError, APITimeoutError

from config import OPENAI_MODEL, OPENAI_TEMPERATURE
from schemas.assessment import RepoAssessmentLLM
from services.openai_client import get_openai_client
from services.prompts import SYSTEM_PROMPT, build_user_message
from schemas.assessment import RepoAssessment


def _has_assessable_readme(repo: dict) -> bool:
    """
    True only when Phase 2 found a README with non-empty text.
    Empty file / whitespace-only is treated like no README.
    """
    if not repo.get("has_readme"):
        return False
    text = repo.get("readme_text")
    return bool(text and text.strip())


async def assess_repo_with_llm(repo: dict) -> RepoAssessmentLLM:
    """
      Run one Structured Outputs call for a single repository.
    Raises SDK/network exceptions on failure (handled at batch layer later).
    """
    client = get_openai_client()
    completion = await client.chat.completions.parse(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_message(repo)},
        ],
        response_format=RepoAssessmentLLM,
        temperature=OPENAI_TEMPERATURE,
    )
    message = completion.choices[0].message
    if message.parsed is None:
        refusal = getattr(message, "refusal", None)
        raise ValueError(refusal or "Model returned no parsed assessment")
    return message.parsed


async def assess_single_repo(repo: dict) -> RepoAssessment:
    repo_name = repo["repo_name"]

    if not _has_assessable_readme(repo):
        return build_skipped_no_readme_assessment(repo_name)

    llm_result = await assess_repo_with_llm(repo)

    return RepoAssessment(
        repo_name=repo_name,
        has_readme=True,
        complexity_level=llm_result.complexity_level,
        documentation_quality=llm_result.documentation_quality,
        estimated_experience_signal=llm_result.estimated_experience_signal,
        summary=llm_result.summary,
        assessment_error=None,
    )


def build_skipped_no_readme_assessment(repo_name: str) -> RepoAssessment:
    """
    No LLM call. No invented ratings.
    Missing README is not the same as 'Poor' or 'Beginner' — we had nothing to assess.
    """
    return RepoAssessment(
        repo_name=repo_name,
        has_readme=False,
        complexity_level=None,
        documentation_quality=None,
        estimated_experience_signal=None,
        summary="No README available — assessment skipped.",
        assessment_error=None,
    )


def _format_assessment_error(exc: Exception) -> str:
    """Map SDK exceptions to short, recruiter-safe error messages."""
    if isinstance(exc, RateLimitError):
        return "OpenAI rate limit exceeded. Try again shortly."
    if isinstance(exc, APITimeoutError):
        return "OpenAI request timed out."
    if isinstance(exc, APIConnectionError):
        return "Could not reach OpenAI."
    if isinstance(exc, APIStatusError):
        return f"OpenAI API error (HTTP {exc.status_code})."
    return str(exc)


def build_failed_assessment(repo: dict, error_message: str) -> RepoAssessment:
    """
    Per-repo failure row — no invented ratings (same principle as no-README skip).
    """
    return RepoAssessment(
        repo_name=repo["repo_name"],
        has_readme=repo.get("has_readme", False),
        complexity_level=None,
        documentation_quality=None,
        estimated_experience_signal=None,
        summary="Assessment could not be completed.",
        assessment_error=error_message,
    )


async def assess_repos_batch(repos: list[dict]) -> list[RepoAssessment]:
    """
    Assess all repos concurrently.
    One repo's failure does not fail the batch (return_exceptions=True).
    """
    tasks = [assess_single_repo(repo) for repo in repos]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    assessments: list[RepoAssessment] = []
    for repo, result in zip(repos, results):
        if isinstance(result, Exception):
            error_message = _format_assessment_error(result)
            assessments.append(build_failed_assessment(repo, error_message))
        else:
            assessments.append(result)
    return assessments
