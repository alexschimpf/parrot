from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(
    prefix='/health',
    tags=['health']
)


@router.get('', response_class=PlainTextResponse)
def get_health() -> str:
    return 'Ok'
