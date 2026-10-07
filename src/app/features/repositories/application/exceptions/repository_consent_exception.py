class RepositoryConsentException(Exception):
    """Base exception for repository consent operations."""
    pass


class RepositoryConsentNotFoundException(RepositoryConsentException):
    """Exception raised when repository consent record is not found."""
    pass


class RepositoryConsentAlreadyExistsException(RepositoryConsentException):
    """Exception raised when trying to create a repository consent that already exists."""
    pass


class InvalidRepositoryUrlException(RepositoryConsentException):
    """Exception raised when repository URL is invalid."""
    pass


class ConsentNotGrantedException(RepositoryConsentException):
    """Exception raised when attempting an operation that requires consent but consent hasn't been granted."""
    pass
