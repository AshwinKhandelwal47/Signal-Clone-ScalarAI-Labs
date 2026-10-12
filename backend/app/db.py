<<<<<<< HEAD
from collections.abc import Iterator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

engine = create_engine(
    get_settings().database_url,
    # FastAPI may use the session from different threads within one request.
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def _set_sqlite_pragmas(dbapi_connection, _record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")  # SQLite ignores FKs unless enabled per connection
    cursor.execute("PRAGMA journal_mode=WAL")  # readers don't block the writer
    cursor.execute("PRAGMA busy_timeout=5000")
    cursor.close()


SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
=======
"""Database connection, SQLite configuration, and session management.

Configures SQLite with WAL journal mode, busy timeouts, and enforced foreign keys.
Provides the DeclarativeBase and FastAPI session dependency generator.
"""

from collections.abc import Iterator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

# SQLite engine with disabled same-thread checks to allow FastAPI dependency injection across threads.
engine = create_engine(
    get_settings().database_url,
    # FastAPI may use the session from different threads within one request.
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def _set_sqlite_pragmas(dbapi_connection, _record) -> None:
    """Enforces essential SQLite PRAGMAs on every new database connection.

    - foreign_keys=ON: SQLite ignores FOREIGN KEY constraints by default unless explicitly activated.
    - journal_mode=WAL: Write-Ahead Logging allows concurrent readers without blocking the active writer.
    - busy_timeout=5000: Milliseconds to wait on file locks before raising OperationalError.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")  # SQLite ignores FKs unless enabled per connection
    cursor.execute("PRAGMA journal_mode=WAL")  # readers don't block the writer
    cursor.execute("PRAGMA busy_timeout=5000")
    cursor.close()


# Session factory: autoflush=False avoids premature flushes before commit; expire_on_commit=False
# keeps loaded attributes accessible after commit without triggering lazy re-queries.
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base declarative class for all SQLAlchemy ORM models."""

    pass


def get_db() -> Iterator[Session]:
    """FastAPI dependency yielding a scoped database session, guaranteed to close on exit."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

>>>>>>> 653fe1e (commented code)
