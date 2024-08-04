import contextlib
from fastapi import Request
from sqlalchemy import text
from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from pyfuta import config


engine = create_engine(config.database_url, echo=True)
async_engine = create_async_engine(config.database_url.replace("sqlite://", "sqlite+aiosqlite://"))


async def drop_def_tables():
    async with async_engine.begin() as conn:
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        [await conn.execute(text(f"DROP TABLE {table_name}")) for (table_name,) in result if table_name.startswith("def_")]


async def create_db_and_tables(engine):
    # make sure all models are imported (keep its record in metadata)

    import pyfuta.app.pages.models as models
    import pyfuta.app.reports.models as models
    import pyfuta.app.reports.builder as reports
    import pyfuta.app.pages.builder as pages

    await drop_def_tables()  # drop all def tables, we will recreate them
    models.metadata.create_all(engine)  # tricks the linter
    await reports.metadata.create_all()
    await pages.metadata.create_all()


# https://stackoverflow.com/questions/75487025/how-to-avoid-creating-multiple-sessions-when-using-fastapi-dependencies-with-sec
def register_middleware(asgi_app):
    @asgi_app.middleware("http")
    async def session_middleware(request: Request, call_next):
        with Session(engine, expire_on_commit=False) as session:
            request.state.session = session
            response = await call_next(request)
            return response


def require_session(request: Request):
    return request.state.session


@contextlib.contextmanager
def session_ctx():
    with Session(engine, expire_on_commit=False) as session:
        yield session


@contextlib.asynccontextmanager
async def async_session_ctx():
    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        yield session
