from src.app.features.projects.domain.repositories.project_repository import ProjectRepository
from src.app.features.repositories.application.exceptions.repository_consent_exception import RepositoryConsentNotFoundException
from src.app.features.repositories.domain.repositories.repository_consent_repository import RepositoryConsentRepository
from src.shared.domain.value_objects.entity_id import EntityId


class UnlinkRepositoryUseCase:
    """Use case for unlinking a repository from a project."""

    def __init__(
        self,
        repository_consent_repository: RepositoryConsentRepository,
        project_repository: ProjectRepository,
    ):
        self.repository_consent_repository = repository_consent_repository
        self.project_repository = project_repository

    async def execute(self, project_id: str, user_id: str) -> None:
        """Unlink a repository from a project.

        Args:
            project_id: ID of the project.
            user_id: ID of the user making the request.

        Raises:
            ProjectNotFoundException: If the project doesn't exist.
            ProjectAccessDeniedException: If user doesn't own the project.
            RepositoryConsentNotFoundException: If no repository linked.
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
            raise ProjectAccessDeniedException("You don't have permission to unlink repository from this project", user_id)

        # Get consent record
        consent = await self.repository_consent_repository.find_by_project_id(project_entity_id)
        if not consent:
            raise RepositoryConsentNotFoundException(
                f"No repository linked to project {project_id}"
            )

        # Delete consent record
        await self.repository_consent_repository.delete(consent.id)
