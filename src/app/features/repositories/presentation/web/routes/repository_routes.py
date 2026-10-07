from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.app.features.auth.presentation.web.dependencies import get_current_user
from src.app.features.projects.application.exceptions.project_exception import (
    ProjectAccessDeniedException,
    ProjectNotFoundException,
)
from src.app.features.repositories.application.dtos.repository_consent_dto import (
    GrantConsentRequest,
    LinkRepositoryRequest,
    RepositoryConsentResponse,
)
from src.app.features.repositories.application.exceptions.repository_consent_exception import (
    InvalidRepositoryUrlException,
    RepositoryConsentAlreadyExistsException,
    RepositoryConsentNotFoundException,
)
from src.app.features.repositories.application.use_cases.get_repository_consent import GetRepositoryConsentUseCase
from src.app.features.repositories.application.use_cases.grant_consent import GrantConsentUseCase
from src.app.features.repositories.application.use_cases.link_repository import LinkRepositoryUseCase
from src.app.features.repositories.application.use_cases.unlink_repository import UnlinkRepositoryUseCase
from src.app.features.repositories.presentation.web.dependencies import (
    get_get_repository_consent_use_case,
    get_grant_consent_use_case,
    get_link_repository_use_case,
    get_unlink_repository_use_case,
)

router = APIRouter()


@router.post(
    "/{project_id}/repository",
    response_model=RepositoryConsentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def link_repository(
    project_id: UUID,
    payload: LinkRepositoryRequest,
    current_user=Depends(get_current_user),
    use_case: LinkRepositoryUseCase = Depends(get_link_repository_use_case),
) -> RepositoryConsentResponse:
    """Link a repository to a project."""
    try:
        return await use_case.execute(str(project_id), current_user.id, payload)
    except ProjectNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ProjectAccessDeniedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except RepositoryConsentAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InvalidRepositoryUrlException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{project_id}/repository",
    response_model=RepositoryConsentResponse,
)
async def get_repository_consent(
    project_id: UUID,
    current_user=Depends(get_current_user),
    use_case: GetRepositoryConsentUseCase = Depends(get_get_repository_consent_use_case),
) -> RepositoryConsentResponse:
    """Get repository consent status for a project."""
    try:
        return await use_case.execute(str(project_id), current_user.id)
    except RepositoryConsentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{project_id}/repository/consent",
    response_model=RepositoryConsentResponse,
)
async def grant_consent(
    project_id: UUID,
    payload: GrantConsentRequest,
    current_user=Depends(get_current_user),
    use_case: GrantConsentUseCase = Depends(get_grant_consent_use_case),
) -> RepositoryConsentResponse:
    """Grant or revoke consent for repository analysis."""
    try:
        return await use_case.execute(str(project_id), current_user.id, payload)
    except RepositoryConsentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{project_id}/repository",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unlink_repository(
    project_id: UUID,
    current_user=Depends(get_current_user),
    use_case: UnlinkRepositoryUseCase = Depends(get_unlink_repository_use_case),
) -> None:
    """Unlink a repository from a project."""
    try:
        await use_case.execute(str(project_id), current_user.id)
    except ProjectNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ProjectAccessDeniedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except RepositoryConsentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
