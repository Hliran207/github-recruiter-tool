from typing import Literal, Optional

from pydantic import BaseModel, Field

ComplexityLevel = Literal["Beginner", "Intermediate", "Advanced"]
DocumentationQuality = Literal["Poor", "Adequate", "Excellent"]


class RepoAssessmentLLM(BaseModel):
    """
    Schema sent to OpenAI Structured Outputs.
    Only fields the model should infer — not ground-truth repo facts.
    """

    complexity_level: ComplexityLevel = Field(
        ...,
        description=(
            "Technical complexity relative to typical public portfolio projects. "
            "Use Advanced only with strong explicit evidence. "
            "Intermediate is normal for solid portfolio work."
        ),
    )
    documentation_quality: DocumentationQuality = Field(
        ...,
        description=(
            "README clarity and completeness for a recruiter. "
            "Poor if missing or nearly empty. Do not reward marketing language without substance."
        ),
    )
    estimated_experience_signal: str = Field(
        ...,
        description=(
            "One short sentence on seniority signal based only on documented evidence. "
            "Be conservative; do not assume unstated skills."
        ),
        min_length=10,
        max_length=200,
    )
    summary: str = Field(
        ...,
        description=(
            "One to two factual sentences for a technical recruiter. "
            "Mention concrete observations from the README/metadata."
        ),
        min_length=20,
        max_length=400,
    )


class RepoAssessment(BaseModel):
    """
    Full per-repo assessment returned by the API (LLM output + Phase 2 facts).
    When has_readme is False, judgment fields are null — we do not invent ratings.
    """

    repo_name: str
    has_readme: bool
    complexity_level: Optional[ComplexityLevel] = None
    documentation_quality: Optional[DocumentationQuality] = None
    estimated_experience_signal: Optional[str] = None
    summary: str
    assessment_error: Optional[str] = None


class CandidateAnalysisResponse(BaseModel):
    """Full API response for GET /api/analyze/{username}."""

    username: str
    profile_url: str
    public_repos: int = Field(
        ..., description="Total public repos on the GitHub profile"
    )
    repos_analyzed: int = Field(
        ..., description="Repos returned after fork filter + cap (assessed or skipped)"
    )
    assessments: list[RepoAssessment]
