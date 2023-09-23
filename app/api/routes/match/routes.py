import json
from typing import Any
from fastapi import Request, Response, APIRouter

from app.service.mock.mock_matcher import MockMatcher
from app.api.exceptions.exceptions import NotFoundException, InvalidResponseHandlerException

router = APIRouter(
    prefix='/match',
    tags=['match'],
    include_in_schema=False
)


@router.get('/{path:path}')
@router.post('/{path:path}')
@router.patch('/{path:path}')
@router.put('/{path:path}')
@router.delete('/{path:path}')
@router.options('/{path:path}')
@router.head('/{path:path}')
async def get_mock_match(request: Request, path: str) -> Response:
    mock = MockMatcher.get_matching_mock(
        method=request.method,
        path=path,
        query_params=request.query_params,
        headers=request.headers,
        cookies=request.cookies
    )
    if not mock:
        raise NotFoundException

    if mock.response_handler:
        program = compile(mock.response_handler, '', 'exec')
        globals_ = {
            'json': json
        }
        locals_ = {
            'method': request.method,
            'path': f'/{path}',
            'query_params': request.query_params,
            'headers': request.headers,
            'cookies': request.cookies,
            'body': await request.body(),
            'response': None
        }
        exec(program, globals_, locals_)
        response_: Any = locals_['response']

        if not response_:
            raise InvalidResponseHandlerException

        mock.response_body = response_['body']
        mock.response_status = response_.get('status', mock.response_status)
        mock.response_headers = response_.get('headers', mock.response_headers)

    if not mock.response_headers:
        mock.response_headers = {}
    if isinstance(mock.response_body, (list, dict)):
        mock.response_body = json.dumps(mock.response_body)
        mock.response_headers['Content-Type'] = 'application/json'
    if not mock.response_headers.get('Content-Type'):
        mock.response_headers['Content-Type'] = 'plain/text'

    return Response(
        content=mock.response_body,
        status_code=mock.response_status or 200,
        headers=mock.response_headers
    )
