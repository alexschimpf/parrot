import json
from typing import Any
from fastapi import Request, Response, APIRouter

from app.service.rule_matcher import RuleMatcher
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
async def get_mock_response(request: Request, path: str) -> Response:
    rule = RuleMatcher.get_matching_rule(
        method=request.method,
        path=path,
        query_params=request.query_params,
        headers=request.headers,
        cookies=request.cookies
    )
    if not rule:
        raise NotFoundException

    if rule.response_handler:
        program = compile(rule.response_handler, '', 'exec')
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

        rule.response_body = response_['body']
        rule.response_status = response_.get('status', rule.response_status)
        rule.response_headers = response_.get('headers', rule.response_headers)

    if not rule.response_headers:
        rule.response_headers = {}
    if isinstance(rule.response_body, (list, dict)):
        rule.response_body = json.dumps(rule.response_body)
        rule.response_headers['Content-Type'] = 'application/json'
    if not rule.response_headers.get('Content-Type'):
        rule.response_headers['Content-Type'] = 'plain/text'

    return Response(
        content=rule.response_body,
        status_code=rule.response_status or 200,
        headers=rule.response_headers
    )
