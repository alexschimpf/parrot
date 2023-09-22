import os
import json
import logging
import logging.config
from typing import Any
import fastapi.openapi.utils
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware

from app.api.exceptions.handlers import get_exception_handlers
from app.api.schemas import ErrorResponseModel
from app.service.mock.mock_manager import MockManager


class Bootstrap:

    def run(self) -> FastAPI:
        self._init_logger()
        self._init_services()

        app = self._build_app()
        self._register_routes(app=app)
        self._override_openapi(app=app)
        self._add_cors_middleware(app=app)
        self._set_route_operation_ids(app=app)

        return app

    @staticmethod
    def _init_logger() -> None:
        config_file_path = os.path.join(os.path.dirname(__file__), 'config/logger.json')
        with open(config_file_path, 'r') as f:
            logger_config = json.loads(f.read())
            logging.config.dictConfig(config=logger_config)

    @classmethod
    def _build_app(cls) -> FastAPI:
        return FastAPI(
            title='Parrot API',
            version='1.0',
            responses={
                400: {'model': ErrorResponseModel}
            },
            exception_handlers=get_exception_handlers(),
            swagger_ui_parameters={'defaultModelsExpandDepth': -1}
        )

    @staticmethod
    def _init_services():
        MockManager.load_mocks()

    @staticmethod
    def _register_routes(app: FastAPI) -> None:
        from app.api import router
        app.include_router(router.router)

    @staticmethod
    def _override_openapi(app: FastAPI) -> None:
        def openapi() -> dict[str, Any]:
            openapi_schema = fastapi.openapi.utils.get_openapi(
                title=app.title,
                version=app.version,
                routes=app.routes
            )

            # Remove 422 response from schema
            for schema_path in openapi_schema['paths']:
                for method in openapi_schema['paths'][schema_path]:
                    openapi_schema['paths'][schema_path][method]['responses'].pop('422', None)

            return openapi_schema

        app.openapi = openapi  # type: ignore

    @staticmethod
    def _set_route_operation_ids(app: FastAPI) -> None:
        for route in app.routes:
            if isinstance(route, APIRoute):
                route.operation_id = route.name

    @staticmethod
    def _add_cors_middleware(app: FastAPI) -> None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
