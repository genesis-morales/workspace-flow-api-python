from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.features.projects.infrastructure.repository.project_repository_impl import ProjectRepositoryImpl
from src.app.features.repositories.application.use_cases.get_repository_consent import GetRepositoryConsentUseCase
from src.app.features.repositories.application.use_cases.grant_consent import GrantConsentUseCase
from src.app.features.repositories.application.use_cases.link_repository import LinkRepositoryUseCase
from src.app.features.repositories.application.use_cases.unlink_repository import UnlinkRepositoryUseCase
from src.app.features.repositories.infrastructure.repository.repository_consent_repository_impl import RepositoryConsentRepositoryImpl
from src.shared.infrastructure.database.session import get_db


def get_link_repository_use_case(session: AsyncSession = Depends(get_db)) -> LinkRepositoryUseCase:
    """Dependency for LinkRepositoryUseCase."""
    repository_consent_repo = RepositoryConsentRepositoryImpl(session)
    project_repo = ProjectRepositoryImpl(session)
    return LinkRepositoryUseCase(repository_consent_repo, project_repo)


def get_get_repository_consent_use_case(session: AsyncSession = Depends(get_db)) -> GetRepositoryConsentUseCase:
    """Dependency for GetRepositoryConsentUseCase."""
    repository_consent_repo = RepositoryConsentRepositoryImpl(session)
    return GetRepositoryConsentUseCase(repository_consent_repo)


def get_grant_consent_use_case(session: AsyncSession = Depends(get_db)) -> GrantConsentUseCase:
    """Dependency for GrantConsentUseCase."""
    repository_consent_repo = RepositoryConsentRepositoryImpl(session)
    return GrantConsentUseCase(repository_consent_repo)


def get_unlink_repository_use_case(session: AsyncSession = Depends(get_db)) -> UnlinkRepositoryUseCase:
    """Dependency for UnlinkRepositoryUseCase."""
    repository_consent_repo = RepositoryConsentRepositoryImpl(session)
    project_repo = ProjectRepositoryImpl(session)
    return UnlinkRepositoryUseCase(repository_consent_repo, project_repo)
