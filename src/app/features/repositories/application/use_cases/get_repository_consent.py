from src.app.features.repositories.application.dtos.repository_consent_dto import RepositoryConsentResponse
from src.app.features.repositories.application.dtos.repository_consent_dto_mapper import RepositoryConsentDtoMapper
from src.app.features.repositories.application.exceptions.repository_consent_exception import RepositoryConsentNotFoundException
from src.app.features.repositories.domain.repositories.repository_consent_repository import RepositoryConsentRepository
from src.shared.domain.value_objects.entity_id import EntityId


class GetRepositoryConsentUseCase:
    """Use case for getting repository consent status."""

    def __init__(self, repository_consent_repository: RepositoryConsentRepository):
        self.repository_consent_repository = repository_consent_repository
        self.mapper = RepositoryConsentDtoMapper()

    async def execute(self, project_id: str, user_id: str) -> RepositoryConsentResponse:
        """Get repository consent status for a project.

        Args:
            project_id: ID of the project.
            user_id: ID of the user making the request.

        Returns:
            RepositoryConsentResponse with consent details.

        Raises:
            RepositoryConsentNotFoundException: If no repository linked.
        """
        project_entity_id = EntityId.from_string(project_id)

        consent = await self.repository_consent_repository.find_by_project_id(project_entity_id)
        if not consent:
            raise RepositoryConsentNotFoundException(
                f"No repository linked to project {project_id}"
            )

        return self.mapper.to_response(consent)
