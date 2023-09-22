from http import HTTPStatus
from fastapi import APIRouter, Response
from dataclasses import asdict

from app.service.mock.mock_manager import MockManager, Mock
from app.api.exceptions.exceptions import NotFoundException
from app.api.routes.mocks import schemas
from app.api.schemas import SuccessResponse

router = APIRouter(
    prefix='/mocks',
    tags=['mocks']
)


@router.get('')
def get_mocks() -> schemas.Mocks:
    mocks = MockManager.get_mocks()
    return schemas.Mocks(mocks=[
        schemas.Mock(**asdict(mock)) for mock in mocks
    ])


@router.put('')
def create_or_replace_mock(mock_body: schemas.Mock, response: Response) -> SuccessResponse:
    updated = MockManager.add_or_update_mock(Mock(**mock_body.model_dump()))
    if not updated:
        response.status_code = HTTPStatus.CREATED
    return SuccessResponse(success=True)


@router.get('/{name}')
def get_mock(name: str) -> schemas.Mock:
    mock = MockManager.get_mock(name=name)
    if not mock:
        raise NotFoundException

    return schemas.Mock(**asdict(mock))


@router.put('/{name}')
def update_mock(name: str, mock_body: schemas.Mock) -> SuccessResponse:
    if not MockManager.get_mock(name=name):
        raise NotFoundException

    MockManager.add_or_update_mock(mock=Mock(**mock_body.model_dump()))
    return SuccessResponse(success=True)


@router.delete('/{name}')
def remove_mock(name: str) -> SuccessResponse:
    if not MockManager.get_mock(name=name):
        raise NotFoundException

    MockManager.remove_mock(name=name)
    return SuccessResponse(success=True)
