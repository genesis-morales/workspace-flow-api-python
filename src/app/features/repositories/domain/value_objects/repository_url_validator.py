import re


class RepositoryUrlValidator:
    """Validator for repository URLs."""

    GITHUB_PATTERN = re.compile(
        r'^https?://github\.com/[\w-]+/[\w.-]+/?$'
    )

    @classmethod
    def is_valid_github_url(cls, url: str) -> bool:
        """Check if the URL is a valid GitHub repository URL."""
        return bool(cls.GITHUB_PATTERN.match(url))

    @classmethod
    def validate(cls, repository_type: str, repository_url: str) -> None:
        """Validate repository URL based on type.

        Raises:
            ValueError: If the URL is invalid for the given type.
        """
        if repository_type == "github":
            if not cls.is_valid_github_url(repository_url):
                raise ValueError(
                    "Invalid GitHub repository URL. Expected format: "
                    "https://github.com/username/repository"
                )
        elif repository_type == "local":
            if not repository_url or len(repository_url.strip()) == 0:
                raise ValueError("Local repository path cannot be empty")
