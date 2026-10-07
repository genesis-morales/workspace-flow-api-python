from src.app.features.repositories.application.dtos.repository_consent_dto import GrantConsentRequest, RepositoryConsentResponse
from src.app.features.repositories.application.dtos.repository_consent_dto_mapper import RepositoryConsentDtoMapper
from src.app.features.repositories.application.exceptions.repository_consent_exception import RepositoryConsentNotFoundException
from src.app.features.repositories.domain.repositories.repository_consent_repository import RepositoryConsentRepository
from src.shared.domain.value_objects.entity_id import EntityId


class GrantConsentUseCase:
    """Use case for granting or revoking repository analysis consent."""

    def __init__(self, repository_consent_repository: RepositoryConsentRepository):
        self.repository_consent_repository = repository_consent_repository
        self.mapper = RepositoryConsentDtoMapper()

    async def execute(
        self,
        project_id: str,
        user_id: str,
        request: GrantConsentRequest,
    ) -> RepositoryConsentResponse:
        """Grant or revoke consent for repository analysis.

        Args:
            project_id: ID of the project.
            user_id: ID of the user making the request.
            request: Request containing consent status.

        Returns:
            RepositoryConsentResponse with updated consent.

        Raises:
            RepositoryConsentNotFoundException: If no repository linked.
        """
        project_entity_id = EntityId.from_string(project_id)

        consent = await self.repository_consent_repository.find_by_project_id(project_entity_id)
        if not consent:
            raise RepositoryConsentNotFoundException(
                f"No repository linked to project {project_id}"
            )

        if request.consent_given:
            consent.grant_consent()
        else:
            consent.revoke_consent()

        saved_consent = await self.repository_consent_repository.save(consent)

        return self.mapper.to_response(saved_consent)
