from src.app.features.projects.domain.repositories.project_repository import ProjectRepository
from src.app.features.repositories.application.dtos.repository_consent_dto import LinkRepositoryRequest, RepositoryConsentResponse
from src.app.features.repositories.application.dtos.repository_consent_dto_mapper import RepositoryConsentDtoMapper
from src.app.features.repositories.application.exceptions.repository_consent_exception import (
    InvalidRepositoryUrlException,
    RepositoryConsentAlreadyExistsException,
)
from src.app.features.repositories.domain.entities.repository_consent_entity import RepositoryConsentEntity
from src.app.features.repositories.domain.entities.repository_type import RepositoryType
from src.app.features.repositories.domain.repositories.repository_consent_repository import RepositoryConsentRepository
from src.app.features.repositories.domain.value_objects.repository_url_validator import RepositoryUrlValidator
from src.shared.domain.value_objects.entity_id import EntityId


class LinkRepositoryUseCase:
    """Use case for linking a repository to a project."""

    def __init__(
        self,
        repository_consent_repository: RepositoryConsentRepository,
        project_repository: ProjectRepository,
    ):
        self.repository_consent_repository = repository_consent_repository
        self.project_repository = project_repository
        self.mapper = RepositoryConsentDtoMapper()

    async def execute(
        self,
        project_id: str,
        user_id: str,
        request: LinkRepositoryRequest,
    ) -> RepositoryConsentResponse:
        """Link a repository to a project.

        Args:
            project_id: ID of the project to link the repository to.
            user_id: ID of the user making the request.
            request: Request containing repository type and URL.

        Returns:
            RepositoryConsentResponse with the created consent record.

        Raises:
            ProjectNotFoundException: If the project doesn't exist.
            ProjectAccessDeniedException: If user doesn't own the project.
            RepositoryConsentAlreadyExistsException: If repository already linked.
            InvalidRepositoryUrlException: If the repository URL is invalid.
        """
        project_entity_id = EntityId.from_string(project_id)
        user_entity_id = EntityId.from_string(user_id)

        # Verify project exists and user owns it
        project = await self.project_repository.find_by_id(project_entity_id)
        if not project:
            from src.app.features.projects.application.exceptions.project_exception import ProjectNotFoundException
            raise ProjectNotFoundException(f"Project with id {project_id} not found")

        if project.owner_id != user_entity_id:
            from src.app.features.projects.application.exceptions.project_exception import ProjectAccessDeniedException
            raise ProjectAccessDeniedException("You don't have permission to link a repository to this project", user_id)

        # Check if repository consent already exists
        existing_consent = await self.repository_consent_repository.find_by_project_id(project_entity_id)
        if existing_consent:
            raise RepositoryConsentAlreadyExistsException(
                f"Repository already linked to project {project_id}. Delete existing link first."
            )

        # Validate repository URL
        try:
            RepositoryUrlValidator.validate(request.repository_type, request.repository_url)
        except ValueError as e:
            raise InvalidRepositoryUrlException(str(e))

        # Create repository consent entity (without consent granted yet)
        repository_type = RepositoryType(request.repository_type)
        consent_entity = RepositoryConsentEntity(
            project_id=project_entity_id,
            repository_type=repository_type,
            repository_url=request.repository_url,
            consent_given=False,
        )

        # Save to database
        saved_entity = await self.repository_consent_repository.save(consent_entity)

        return self.mapper.to_response(saved_entity)
