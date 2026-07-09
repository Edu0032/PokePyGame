from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


def normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql://", 1)
    return database_url


def create_database_engine(database_url: str) -> Engine:
    normalized_url = normalize_database_url(database_url)
    if normalized_url.startswith("sqlite"):
        return create_engine(
            normalized_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            future=True,
        )
    return create_engine(normalized_url, pool_pre_ping=True, future=True)


def create_session_factory(engine: Engine) -> sessionmaker:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def create_tables(engine: Engine) -> None:
    from PokePY.infrastructure.sqlalchemy import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
