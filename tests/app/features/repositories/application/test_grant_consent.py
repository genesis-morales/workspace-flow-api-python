import pytest
from unittest.mock import AsyncMock
from uuid import UUID

from src.app.features.repositories.application.dtos.repository_consent_dto import GrantConsentRequest
from src.app.features.repositories.application.exceptions.repository_consent_exception import RepositoryConsentNotFoundException
from src.app.features.repositories.application.use_cases.grant_consent import GrantConsentUseCase
from src.app.features.repositories.domain.entities.repository_consent_entity import RepositoryConsentEntity
from src.app.features.repositories.domain.entities.repository_type import RepositoryType
from src.shared.domain.value_objects.entity_id import EntityId


@pytest.fixture
def mock_consent_repo():
    return AsyncMock()


@pytest.fixture
def grant_consent_use_case(mock_consent_repo):
    return GrantConsentUseCase(mock_consent_repo)


@pytest.fixture
def consent_entity():
    return RepositoryConsentEntity(
        id=EntityId(UUID("550e8400-e29b-41d4-a716-446655440000")),
        project_id=EntityId(UUID("550e8400-e29b-41d4-a716-446655440001")),
        repository_type=RepositoryType.GITHUB,
        repository_url="https://github.com/user/repo",
        consent_given=False,
    )


class TestGrantConsentUseCase:
    @pytest.mark.asyncio
    async def test_grants_consent_successfully(
        self, grant_consent_use_case, mock_consent_repo, consent_entity
    ):
        # Arrange
        mock_consent_repo.find_by_project_id.return_value = consent_entity
        mock_consent_repo.save.return_value = consent_entity

        request = GrantConsentRequest(consentGiven=True)

        # Act
        result = await grant_consent_use_case.execute("550e8400-e29b-41d4-a716-446655440001", "550e8400-e29b-41d4-a716-446655440002", request)

        # Assert
        assert result.consent_given is True
        assert result.consent_given_at is not None
        mock_consent_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_revokes_consent_successfully(
        self, grant_consent_use_case, mock_consent_repo
    ):
        # Arrange
        consent_entity = RepositoryConsentEntity(
            id=EntityId(UUID("550e8400-e29b-41d4-a716-446655440000")),
            project_id=EntityId(UUID("550e8400-e29b-41d4-a716-446655440001")),
            repository_type=RepositoryType.GITHUB,
            repository_url="https://github.com/user/repo",
            consent_given=True,
        )
        mock_consent_repo.find_by_project_id.return_value = consent_entity
        mock_consent_repo.save.return_value = consent_entity

        request = GrantConsentRequest(consentGiven=False)

        # Act
        result = await grant_consent_use_case.execute("550e8400-e29b-41d4-a716-446655440001", "550e8400-e29b-41d4-a716-446655440002", request)

        # Assert
        assert result.consent_given is False
        assert result.consent_given_at is None
        mock_consent_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_raises_not_found_when_no_repository_linked(
        self, grant_consent_use_case, mock_consent_repo
    ):
        # Arrange
        mock_consent_repo.find_by_project_id.return_value = None
        request = GrantConsentRequest(consentGiven=True)

        # Act & Assert
        with pytest.raises(RepositoryConsentNotFoundException):
            await grant_consent_use_case.execute("550e8400-e29b-41d4-a716-446655440001", "550e8400-e29b-41d4-a716-446655440002", request)
