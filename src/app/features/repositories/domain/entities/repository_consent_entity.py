from datetime import datetime
from typing import Optional

from src.app.features.repositories.domain.entities.repository_type import RepositoryType
from src.shared.domain.entities.base_entity import BaseEntity
from src.shared.domain.value_objects.entity_id import EntityId


class RepositoryConsentEntity(BaseEntity):
    """Domain entity representing repository consent for analysis.

    Attributes:
        id: Unique identifier for the consent record.
        project_id: EntityId of the project this consent belongs to.
        repository_type: Type of repository (github or local).
        repository_url: URL or path of the repository.
        consent_given: Whether consent has been granted.
        consent_given_at: Timestamp when consent was granted (None if not yet given).
        created_at: Timestamp when the record was created.
        updated_at: Timestamp when the record was last updated.
    """

    def __init__(
        self,
        project_id: EntityId,
        repository_type: RepositoryType,
        repository_url: str,
        consent_given: bool = False,
        consent_given_at: Optional[datetime] = None,
        id: EntityId = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.project_id: EntityId = project_id
        self.repository_type: RepositoryType = repository_type
        self.repository_url: str = repository_url
        self.consent_given: bool = consent_given
        self.consent_given_at: Optional[datetime] = consent_given_at

    def grant_consent(self) -> None:
        """Grant consent for repository analysis."""
        self.consent_given = True
        self.consent_given_at = datetime.now()
        self.mark_as_updated()

    def revoke_consent(self) -> None:
        """Revoke consent for repository analysis."""
        self.consent_given = False
        self.consent_given_at = None
        self.mark_as_updated()

    def update_repository_url(self, repository_url: str) -> None:
        """Update the repository URL."""
        self.repository_url = repository_url
        self.mark_as_updated()
