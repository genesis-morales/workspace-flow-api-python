from abc import ABC, abstractmethod
from typing import Optional

from src.app.features.repositories.domain.entities.repository_consent_entity import RepositoryConsentEntity
from src.shared.domain.value_objects.entity_id import EntityId


class RepositoryConsentRepository(ABC):
    """Abstract repository for repository consent operations."""

    @abstractmethod
    async def save(self, consent: RepositoryConsentEntity) -> RepositoryConsentEntity:
        """Save or update a repository consent record."""
        pass

    @abstractmethod
    async def find_by_id(self, consent_id: EntityId) -> Optional[RepositoryConsentEntity]:
        """Find a repository consent record by its ID."""
        pass

    @abstractmethod
    async def find_by_project_id(self, project_id: EntityId) -> Optional[RepositoryConsentEntity]:
        """Find a repository consent record by project ID."""
        pass

    @abstractmethod
    async def delete(self, consent_id: EntityId) -> None:
        """Delete a repository consent record."""
        pass

    @abstractmethod
    async def exists_by_project_id(self, project_id: EntityId) -> bool:
        """Check if a repository consent record exists for a project."""
        pass
