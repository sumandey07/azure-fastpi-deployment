"""FastAPI application factory.

The app is deployed behind Azure Functions, where HTTP routes are served
under the ``/api`` prefix by default (see host.json ``routePrefix``). Set
``ROOT_PATH=/api`` in the Function App settings so the OpenAPI docs and
generated links resolve correctly. Locally the Functions host also uses
``/api``.
"""
import os

from fastapi import FastAPI

from app.routers import items
from app.schemas import HealthResponse

VERSION = "1.0.0"


def create_app() -> FastAPI:
    app = FastAPI(
        title="Azure FastAPI",
        description="A FastAPI service deployed to Azure Functions.",
        version=VERSION,
        root_path=os.getenv("ROOT_PATH", ""),
    )

    @app.get("/", tags=["root"])
    async def root() -> dict[str, str]:
        return {"message": "Welcome to Azure FastAPI. See /docs for the API."}

    @app.get("/health", response_model=HealthResponse, tags=["health"])
    async def health() -> HealthResponse:
        return HealthResponse(service="azure-fastapi", version=VERSION)

    app.include_router(items.router)
    return app


app = create_app()
