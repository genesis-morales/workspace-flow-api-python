import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

from src.app.features.projects.application.exceptions.project_exception import ProjectAccessDeniedException, ProjectNotFoundException
from src.app.features.repositories.application.dtos.repository_consent_dto import LinkRepositoryRequest
from src.app.features.repositories.application.exceptions.repository_consent_exception import (
    InvalidRepositoryUrlException,
    RepositoryConsentAlreadyExistsException,
)
from src.app.features.repositories.application.use_cases.link_repository import LinkRepositoryUseCase
from src.app.features.repositories.domain.entities.repository_consent_entity import RepositoryConsentEntity
from src.app.features.repositories.domain.entities.repository_type import RepositoryType
from src.app.features.projects.domain.entities.project_entity import ProjectEntity
from src.app.features.projects.domain.entities.project_status import ProjectStatus
from src.shared.domain.value_objects.entity_id import EntityId


@pytest.fixture
def mock_consent_repo():
    return AsyncMock()


@pytest.fixture
def mock_project_repo():
    return AsyncMock()


@pytest.fixture
def link_repository_use_case(mock_consent_repo, mock_project_repo):
    return LinkRepositoryUseCase(mock_consent_repo, mock_project_repo)


@pytest.fixture
def project_entity():
    return ProjectEntity(
        id=EntityId(UUID("550e8400-e29b-41d4-a716-446655440000")),
        name="Test Project",
        description="Test Description",
        owner_id=EntityId(UUID("550e8400-e29b-41d4-a716-446655440001")),
        status=ProjectStatus.ACTIVE,
    )


class TestLinkRepositoryUseCase:
    @pytest.mark.asyncio
    async def test_link_github_repository_successfully(
        self, link_repository_use_case, mock_project_repo, mock_consent_repo, project_entity
    ):
        # Arrange
        mock_project_repo.find_by_id.return_value = project_entity
        mock_consent_repo.find_by_project_id.return_value = None

        saved_consent = RepositoryConsentEntity(
            id=EntityId(UUID("550e8400-e29b-41d4-a716-446655440002")),
            project_id=EntityId(UUID("550e8400-e29b-41d4-a716-446655440000")),
            repository_type=RepositoryType.GITHUB,
            repository_url="https://github.com/user/repo",
            consent_given=False,
        )
        mock_consent_repo.save.return_value = saved_consent

        request = LinkRepositoryRequest(
            repositoryType="github",
            repositoryUrl="https://github.com/user/repo",
        )

        # Act
        result = await link_repository_use_case.execute("550e8400-e29b-41d4-a716-446655440000", "550e8400-e29b-41d4-a716-446655440001", request)

        # Assert
        assert result.repository_type == "github"
        assert result.repository_url == "https://github.com/user/repo"
        assert result.consent_given is False
        mock_consent_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_link_local_repository_successfully(
        self, link_repository_use_case, mock_project_repo, mock_consent_repo, project_entity
    ):
        # Arrange
        mock_project_repo.find_by_id.return_value = project_entity
        mock_consent_repo.find_by_project_id.return_value = None

        saved_consent = RepositoryConsentEntity(
            id=EntityId(UUID("550e8400-e29b-41d4-a716-446655440003")),
            project_id=EntityId(UUID("550e8400-e29b-41d4-a716-446655440000")),
            repository_type=RepositoryType.LOCAL,
            repository_url="/path/to/repo",
            consent_given=False,
        )
        mock_consent_repo.save.return_value = saved_consent

        request = LinkRepositoryRequest(
            repositoryType="local",
            repositoryUrl="/path/to/repo",
        )

        # Act
        result = await link_repository_use_case.execute("550e8400-e29b-41d4-a716-446655440000", "550e8400-e29b-41d4-a716-446655440001", request)

        # Assert
        assert result.repository_type == "local"
        assert result.repository_url == "/path/to/repo"

    @pytest.mark.asyncio
    async def test_raises_project_not_found(
        self, link_repository_use_case, mock_project_repo
    ):
        # Arrange
        mock_project_repo.find_by_id.return_value = None
        request = LinkRepositoryRequest(
            repositoryType="github",
            repositoryUrl="https://github.com/user/repo",
        )

        # Act & Assert
        with pytest.raises(ProjectNotFoundException):
            await link_repository_use_case.execute("550e8400-e29b-41d4-a716-446655440000", "550e8400-e29b-41d4-a716-446655440001", request)

    @pytest.mark.asyncio
    async def test_raises_access_denied_when_not_owner(
        self, link_repository_use_case, mock_project_repo, project_entity
    ):
        # Arrange
        mock_project_repo.find_by_id.return_value = project_entity
        request = LinkRepositoryRequest(
            repositoryType="github",
            repositoryUrl="https://github.com/user/repo",
        )

        # Act & Assert
        with pytest.raises(ProjectAccessDeniedException):
            await link_repository_use_case.execute("550e8400-e29b-41d4-a716-446655440000", "550e8400-e29b-41d4-a716-446655440099", request)

    @pytest.mark.asyncio
    async def test_raises_already_exists_when_repository_already_linked(
        self, link_repository_use_case, mock_project_repo, mock_consent_repo, project_entity
    ):
        # Arrange
        mock_project_repo.find_by_id.return_value = project_entity
        existing_consent = RepositoryConsentEntity(
            id=EntityId(UUID("550e8400-e29b-41d4-a716-446655440004")),
            project_id=EntityId(UUID("550e8400-e29b-41d4-a716-446655440000")),
            repository_type=RepositoryType.GITHUB,
            repository_url="https://github.com/user/old-repo",
            consent_given=True,
        )
        mock_consent_repo.find_by_project_id.return_value = existing_consent

        request = LinkRepositoryRequest(
            repositoryType="github",
            repositoryUrl="https://github.com/user/new-repo",
        )

        # Act & Assert
        with pytest.raises(RepositoryConsentAlreadyExistsException):
            await link_repository_use_case.execute("550e8400-e29b-41d4-a716-446655440000", "550e8400-e29b-41d4-a716-446655440001", request)

    @pytest.mark.asyncio
    async def test_raises_invalid_url_for_github(
        self, link_repository_use_case, mock_project_repo, mock_consent_repo, project_entity
    ):
        # Arrange
        mock_project_repo.find_by_id.return_value = project_entity
        mock_consent_repo.find_by_project_id.return_value = None

        request = LinkRepositoryRequest(
            repositoryType="github",
            repositoryUrl="not-a-valid-github-url",
        )

        # Act & Assert
        with pytest.raises(InvalidRepositoryUrlException):
            await link_repository_use_case.execute("550e8400-e29b-41d4-a716-446655440000", "550e8400-e29b-41d4-a716-446655440001", request)

    @pytest.mark.asyncio
    async def test_raises_invalid_url_for_empty_local_path(
        self, link_repository_use_case, mock_project_repo, mock_consent_repo, project_entity
    ):
        # Arrange
        mock_project_repo.find_by_id.return_value = project_entity
        mock_consent_repo.find_by_project_id.return_value = None

        request = LinkRepositoryRequest(
            repositoryType="local",
            repositoryUrl="",
        )

        # Act & Assert
        with pytest.raises(InvalidRepositoryUrlException):
            await link_repository_use_case.execute("550e8400-e29b-41d4-a716-446655440000", "550e8400-e29b-41d4-a716-446655440001", request)
