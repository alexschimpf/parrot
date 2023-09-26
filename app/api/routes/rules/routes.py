from http import HTTPStatus
from fastapi import APIRouter, Response
from dataclasses import asdict

from app.service.rule_manager import RuleManager, Rule
from app.api.exceptions.exceptions import NotFoundException
from app.api.routes.rules import schemas
from app.api.schemas import SuccessResponse

router = APIRouter(
    prefix='/rules',
    tags=['rules']
)


@router.get('')
def get_rules() -> schemas.Rules:
    rules = RuleManager.get_rules()
    return schemas.Rules(rules=[
        schemas.Rule(**asdict(rule)) for rule in rules
    ])


@router.put('')
def create_or_replace_rule(rule_body: schemas.Rule, response: Response) -> SuccessResponse:
    updated = RuleManager.add_or_update_rule(Rule(**rule_body.model_dump()))
    if not updated:
        response.status_code = HTTPStatus.CREATED
    return SuccessResponse(success=True)


@router.get('/{name}')
def get_rule(name: str) -> schemas.Rule:
    rule = RuleManager.get_rule(name=name)
    if not rule:
        raise NotFoundException

    return schemas.Rule(**asdict(rule))


@router.put('/{name}')
def update_rule(name: str, rule_body: schemas.Rule) -> SuccessResponse:
    if not RuleManager.get_rule(name=name):
        raise NotFoundException

    RuleManager.add_or_update_rule(rule=Rule(**rule_body.model_dump()))
    return SuccessResponse(success=True)


@router.delete('/{name}')
def remove_rule(name: str) -> SuccessResponse:
    if not RuleManager.get_rule(name=name):
        raise NotFoundException

    RuleManager.remove_rule(name=name)
    return SuccessResponse(success=True)
