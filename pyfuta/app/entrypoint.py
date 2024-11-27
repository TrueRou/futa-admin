from __future__ import annotations

from fastapi import FastAPI
from sqlalchemy import text
from starlette.middleware.cors import CORSMiddleware

from pyfuta.app import api, database
from pyfuta.app.database import async_session_ctx
from pyfuta.app.logging import log, Ansi


def init_middlewares(asgi_app: FastAPI) -> None:
    origins = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
    ]

    asgi_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    database.register_middleware(asgi_app)


def init_events(asgi_app: FastAPI) -> None:
    @asgi_app.on_event("startup")
    async def on_startup() -> None:
        async with async_session_ctx() as session:
            await session.execute(text("SELECT 1"))  # Test connection
            await database.create_db_and_tables(database.engine)  # TODO: Sql migration
            log("Startup process complete.", Ansi.LGREEN)

    @asgi_app.on_event("shutdown")
    async def on_shutdown() -> None:
        await database.async_engine.dispose()
        database.engine.dispose()


def init_routes(asgi_app: FastAPI) -> None:
    @asgi_app.get("/")
    async def root():
        return {"message": "Welcome to pyfuta!"}

    asgi_app.include_router(api.router)


def init_api() -> FastAPI:
    """Create & initialize our app."""
    asgi_app = FastAPI()

    init_middlewares(asgi_app)
    init_events(asgi_app)
    init_routes(asgi_app)

    return asgi_app


pyfuta_app = init_api()
