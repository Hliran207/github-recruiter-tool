class GitHubUserNotFoundError(Exception):
    """Raised when GET /users/{username} returns a 404."""

    def __init__(self, username: str):
        self.username = username
        super().__init__(f"GitHub user '{username}' not found")
