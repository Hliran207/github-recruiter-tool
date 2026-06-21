import asyncio

from services.assessment_service import assess_repos_batch


async def main():
    repos = [
        {
            "repo_name": "good-repo",
            "description": "Demo API",
            "language": "Python",
            "stargazers_count": 1,
            "updated_at": "2024-01-01T00:00:00Z",
            "has_readme": True,
            "readme_text": "# Good Repo\n\nCRUD API with setup instructions.",
        },
        {
            "repo_name": "no-readme-repo",
            "description": None,
            "language": "JavaScript",
            "stargazers_count": 0,
            "updated_at": "2023-01-01T00:00:00Z",
            "has_readme": False,
            "readme_text": None,
        },
    ]

    results = await assess_repos_batch(repos)

    for row in results:
        print(
            row.repo_name,
            "| has_readme:",
            row.has_readme,
            "| complexity:",
            row.complexity_level,
            "| error:",
            row.assessment_error,
            "| summary:",
            row.summary[:60],
        )


asyncio.run(main())
