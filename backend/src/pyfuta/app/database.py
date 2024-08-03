import contextlib
from fastapi import Request
from sqlalchemy import func
from sqlmodel import SQLModel, create_engine, Session, select
from sqlmodel.sql.expression import _T0, _TCCA, SelectOfScalar
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from pyfuta import config


engine = create_engine(config.database_url, echo=True)
async_engine = create_async_engine(config.database_url.replace("sqlite://", "sqlite+aiosqlite://"))


async def create_db_and_tables(engine):
    # make sure all models are imported (keep its record in metadata)
    import pyfuta.app.report.models as models
    import pyfuta.app.report.builder as builder

    models.metadata.create_all(engine)
    await builder.metadata.create_all()


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
    async with AsyncSession(async_engine) as session:
        yield session


def count(model: _TCCA[_T0]) -> SelectOfScalar[int]:
    return select(func.count()).select_from(model)


def add_model(session: Session, *models):
    [session.add(model) for model in models if model]
    session.commit()
    [session.refresh(model) for model in models if model]


def partial_update_model(session: Session, item: SQLModel, updates: SQLModel):
    if item and updates:
        update_data = updates.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)
        session.commit()
        session.refresh(item)
