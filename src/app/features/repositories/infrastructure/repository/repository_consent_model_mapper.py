from typing import Optional

from src.app.features.repositories.domain.entities.repository_consent_entity import RepositoryConsentEntity
from src.app.features.repositories.domain.entities.repository_type import RepositoryType
from src.app.features.repositories.infrastructure.models.repository_consent_model import RepositoryConsentModel
from src.shared.domain.value_objects.entity_id import EntityId


class RepositoryConsentModelMapper:
    """Mapper between RepositoryConsentEntity and RepositoryConsentModel."""

    @staticmethod
    def to_entity(model: RepositoryConsentModel) -> RepositoryConsentEntity:
        """Convert SQLAlchemy model to domain entity."""
        return RepositoryConsentEntity(
            id=EntityId(str(model.id)),
            project_id=EntityId(str(model.project_id)),
            repository_type=RepositoryType(model.repository_type),
            repository_url=model.repository_url,
            consent_given=model.consent_given,
            consent_given_at=model.consent_given_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: RepositoryConsentEntity, existing_model: Optional[RepositoryConsentModel] = None) -> RepositoryConsentModel:
        """Convert domain entity to SQLAlchemy model."""
        if existing_model:
            existing_model.project_id = entity.project_id.value
            existing_model.repository_type = entity.repository_type.value
            existing_model.repository_url = entity.repository_url
            existing_model.consent_given = entity.consent_given
            existing_model.consent_given_at = entity.consent_given_at
            existing_model.updated_at = entity.updated_at
            return existing_model

        return RepositoryConsentModel(
            id=entity.id.value if entity.id else None,
            project_id=entity.project_id.value,
            repository_type=entity.repository_type.value,
            repository_url=entity.repository_url,
            consent_given=entity.consent_given,
            consent_given_at=entity.consent_given_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
