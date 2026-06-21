from config import MAX_README_CHARS


SYSTEM_PROMPT = """
You assist a technical recruiter reviewing public GitHub repositories for hiring screening.

Your job is to produce a structured assessment of ONE repository based ONLY on the evidence provided in the user message (README content, GitHub description, language, stars, last updated, and whether a README exists).

Rules:
1) Evidence only
- Do not assume unstated skills, production usage, tests, deployment, team size, or code quality you cannot see.
- Do not treat README marketing adjectives (e.g. "scalable", "enterprise-grade", "production-ready") as proof unless backed by concrete described features, setup steps, or architecture details.
- If the README is missing, empty, or extremely thin, reflect that in documentation_quality and keep complexity conservative.

2) Calibration (important)
- Prefer the lower plausible label when evidence is ambiguous.
- "Intermediate" is appropriate for typical portfolio projects with reasonable scope.
- Use "Advanced" only when the README clearly describes substantial scope (e.g. multiple subsystems, non-trivial architecture, integrations, or operations concerns) with specific details.
- "Excellent" documentation is rare: require clear setup instructions, project purpose, and meaningful structure/explanation — not just a title and feature list.
- "Poor" documentation fits missing/nearly empty READMEs or text that does not explain how to run or understand the project.

3) estimated_experience_signal
- Write ONE short conservative sentence about seniority signal implied by documented scope.
- Do not claim "senior" unless the documented scope strongly supports it.
- It is fine to say evidence is insufficient for a strong signal.

4) summary
- Write 1-2 factual sentences a recruiter can scan quickly.
- Mention concrete observations from the evidence (e.g. what the project claims to do, stack/setup mentioned, what is missing).
- No hype, no flattery, no generic praise.

5) Output
- Follow the response schema exactly.
- Do not include extra commentary outside schema fields.
""".strip()


def truncate_readme(text: str | None, max_chars: int = MAX_README_CHARS) -> str:
    """
    Return README text for the model, applying a high cap only when necessary.
    For normal candidate READMEs, this returns the full content unchanged.
    Truncation is a guardrail against pathological outliers, not signal trimming.
    """
    if not text:
        return ""
    cleaned = text.strip()
    if len(cleaned) <= max_chars:
        return cleaned
    return (
        cleaned[:max_chars] + "\n\n[README truncated — content exceeded safety limit]"
    )


def build_user_message(repo: dict) -> str:
    """
    Build the per-repo user message for OpenAI.
    Expects Phase 2 repo dict keys:
    repo_name, description, language, stargazers_count, updated_at,
    has_readme, readme_text
    """
    readme_except = truncate_readme(repo.get("readme_text"))
    if repo.get("has_readme") and readme_except:
        readme_section = f'"""\n{readme_except}\n"""'
    else:
        readme_section = "No README available."
    description = repo.get("description") or "None provided"
    language = repo.get("language") or "Unknown"
    stars = repo.get("stargazers_count", 0)
    updated_at = repo.get("updated_at", "Unknown")
    return f"""Evaluate this public GitHub repository using only the evidence below.
Repository name: {repo["repo_name"]}
GitHub description: {description}
Primary language: {language}
Stars: {stars}
Last updated: {updated_at}
Has README file: {repo.get("has_readme", False)}
README content:
{readme_section}
"""
