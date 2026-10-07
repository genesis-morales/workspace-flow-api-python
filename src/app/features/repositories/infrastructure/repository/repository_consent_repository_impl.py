from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.features.repositories.domain.entities.repository_consent_entity import RepositoryConsentEntity
from src.app.features.repositories.domain.repositories.repository_consent_repository import RepositoryConsentRepository
from src.app.features.repositories.infrastructure.models.repository_consent_model import RepositoryConsentModel
from src.app.features.repositories.infrastructure.repository.repository_consent_model_mapper import RepositoryConsentModelMapper
from src.shared.domain.value_objects.entity_id import EntityId


class RepositoryConsentRepositoryImpl(RepositoryConsentRepository):
    """SQLAlchemy implementation of RepositoryConsentRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.mapper = RepositoryConsentModelMapper()

    async def save(self, consent: RepositoryConsentEntity) -> RepositoryConsentEntity:
        """Save or update a repository consent record."""
        existing_model = None
        if consent.id:
            result = await self.session.execute(
                select(RepositoryConsentModel).where(RepositoryConsentModel.id == consent.id.value)
            )
            existing_model = result.scalar_one_or_none()

        model = self.mapper.to_model(consent, existing_model)

        if not existing_model:
            self.session.add(model)

        await self.session.flush()
        await self.session.refresh(model)

        return self.mapper.to_entity(model)

    async def find_by_id(self, consent_id: EntityId) -> Optional[RepositoryConsentEntity]:
        """Find a repository consent record by its ID."""
        result = await self.session.execute(
            select(RepositoryConsentModel).where(RepositoryConsentModel.id == consent_id.value)
        )
        model = result.scalar_one_or_none()
        return self.mapper.to_entity(model) if model else None

    async def find_by_project_id(self, project_id: EntityId) -> Optional[RepositoryConsentEntity]:
        """Find a repository consent record by project ID."""
        result = await self.session.execute(
            select(RepositoryConsentModel).where(RepositoryConsentModel.project_id == project_id.value)
        )
        model = result.scalar_one_or_none()
        return self.mapper.to_entity(model) if model else None

    async def delete(self, consent_id: EntityId) -> None:
        """Delete a repository consent record."""
        result = await self.session.execute(
            select(RepositoryConsentModel).where(RepositoryConsentModel.id == consent_id.value)
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()

    async def exists_by_project_id(self, project_id: EntityId) -> bool:
        """Check if a repository consent record exists for a project."""
        result = await self.session.execute(
            select(RepositoryConsentModel.id).where(RepositoryConsentModel.project_id == project_id.value)
        )
        return result.scalar_one_or_none() is not None
