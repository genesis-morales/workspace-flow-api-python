from src.app.features.repositories.application.dtos.repository_consent_dto import RepositoryConsentResponse
from src.app.features.repositories.domain.entities.repository_consent_entity import RepositoryConsentEntity


class RepositoryConsentDtoMapper:
    """Mapper between RepositoryConsentEntity and DTOs."""

    @staticmethod
    def to_response(entity: RepositoryConsentEntity) -> RepositoryConsentResponse:
        """Convert entity to response DTO."""
        return RepositoryConsentResponse(
            id=str(entity.id.value),
            projectId=str(entity.project_id.value),
            repositoryType=entity.repository_type.value,
            repositoryUrl=entity.repository_url,
            consentGiven=entity.consent_given,
            consentGivenAt=entity.consent_given_at,
            createdAt=entity.created_at,
            updatedAt=entity.updated_at,
        )
