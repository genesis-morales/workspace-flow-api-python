from enum import Enum


class RepositoryType(str, Enum):
    """Enum representing the type of repository."""

    GITHUB = "github"
    LOCAL = "local"
