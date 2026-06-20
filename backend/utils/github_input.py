from urllib.parse import urlparse


def normalize_github_username(raw: str) -> str:
    """
    Accept a github username ot profile URL and return a clean username.

    Examples:
        "hliran2: -> "hliran2"
        "@hliran2" -> "hliran2"
        "https://github.com/hliran2" -> "hliran2"
        "https://github.com/hliran2/" -> "hliran2"
        "github.com/hliran2" -> "hliran2"
    """
    value = raw.strip()

    if not value:
        raise ValueError("Username cannot be empty")

    if value.startswith("@"):
        value = value[1:]

    if "github.com" in value.lower():
        if not value.startswith(("https://", "http://")):
            value = f"https://{value}"
        parsed_url = urlparse(value)
        path_parts = [part for part in parsed_url.path.strip("/").split("/") if part]

        if not path_parts:
            raise ValueError("No username found in GitHub URL")

        username = path_parts[0]
    else:
        username = value

    username = username.strip().strip("/")

    if not username:
        raise ValueError("Username cannot be empty")

    return username.lower()
