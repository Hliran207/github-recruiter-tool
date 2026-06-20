from typing import Literal
from pydantic import BaseModel, Field

ComplexityLevel = Literal["low", "medium", "high"]
DocumentationQuality = Literal["poor", "fair", "good", "excellent"]
ExperienceSignal = Literal["junior", "mid", "senior"]


class RepoAssessment(BaseModel):
    """AI-generated assessment of a single public GitHub repository."""

    repo_name: str = Field(
        ...,
        description="Repository name as it appears on GitHub (e.g. 'my-api-project').",
    )
    complexity_level: ComplexityLevel = Field(
        ...,
        description="Technical complexity relative to typical portfolio projects.",
    )
    documentation_quality: DocumentationQuality = Field(
        ...,
        description="How clear and complete the README is for a recruiter or hiring manager.",
    )
    estimated_experience_signal: ExperienceSignal = Field(
        ...,
        description="Rough seniority signal inferred from code scope, README, and project structure.",
    )
    summary: str = Field(
        ...,
        description="2-3 sentence recruiter-friendly summary of what the project demonstrates.",
        min_length=10,
        max_length=500,
    )
    has_readme: bool = Field(
        ...,
        description="Whether a README was found and used for this assessment.",
    )
