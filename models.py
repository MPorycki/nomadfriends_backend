from contextlib import contextmanager

from sqlalchemy import (
    create_engine,
    Column,
    String,
    TIMESTAMP,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, Float
from sqlalchemy.dialects.postgresql import UUID

from config import host, database, user, password

db = create_engine(f"postgresql://{user}:{password}@{host}/{database}")
base = declarative_base()
Session = scoped_session(sessionmaker(db))
session = Session()


@contextmanager
def session_scope(_session=None):
    if _session is None:
        _session = Session()

    try:
        yield _session
        _session.commit()
    except Exception as e:
        _session.rollback()
        raise e
    finally:
        _session.close()


class Users(base):
    """
    Table representing user accounts in the application.
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    created_at = Column(TIMESTAMP)
    first_name = Column(String(length=64), nullable=True)
    last_name = Column(String(length=32), nullable=True)
    display_name = Column(String(length=32), nullable=True)
    avatar = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Sessions(base):
    __tablename__ = "sessions"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(Users.id, onupdate="CASCADE", ondelete="CASCADE"),
    )
    session_id = Column(UUID(as_uuid=True), primary_key=True)
    created_at = Column(TIMESTAMP)


class Places(base):
    __tablename__ = "places"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    lat = Column(Float)
    lng = Column(Float)


class Trips(base):
    __tablename__ = "trips"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(Users.id, onupdate="CASCADE", ondelete="CASCADE"),
    )
    place_id = Column(
        UUID(as_uuid=True),
        ForeignKey(Places.id, onupdate="CASCADE", ondelete="CASCADE"),
    )
    arrival_at = Column(Date, nullable=False)
    departure_at = Column(Date, nullable=True)


base.metadata.create_all(db)
