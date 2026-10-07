from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from src.shared.infrastructure.database.base import Base


class RepositoryConsentModel(Base):
    """SQLAlchemy model for repository consent."""

    __tablename__ = "repository_consent"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True)
    repository_type = Column(String(50), nullable=False)
    repository_url = Column(String(500), nullable=False)
    consent_given = Column(Boolean, nullable=False, default=False)
    consent_given_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
