from fastapi import APIRouter

from app.api.routes.health.routes import router as health_router
from app.api.routes.mocks.routes import router as mock_router
from app.api.routes.match.routes import router as match_router


router = APIRouter()
router.include_router(health_router)
router.include_router(mock_router)
router.include_router(match_router)
