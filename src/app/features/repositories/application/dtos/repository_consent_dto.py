from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RepositoryConsentResponse(BaseModel):
    """Response DTO for repository consent."""
    id: str
    project_id: str = Field(alias="projectId")
    repository_type: str = Field(alias="repositoryType")
    repository_url: str = Field(alias="repositoryUrl")
    consent_given: bool = Field(alias="consentGiven")
    consent_given_at: Optional[datetime] = Field(None, alias="consentGivenAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        populate_by_name = True


class LinkRepositoryRequest(BaseModel):
    """Request DTO for linking a repository to a project."""
    repository_type: str = Field(alias="repositoryType")
    repository_url: str = Field(alias="repositoryUrl")

    class Config:
        populate_by_name = True


class GrantConsentRequest(BaseModel):
    """Request DTO for granting consent."""
    consent_given: bool = Field(alias="consentGiven")

    class Config:
        populate_by_name = True
