from contextlib import contextmanager

from sqlalchemy import (
    create_engine,
    Column,
    String,
    TIMESTAMP,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

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


class Accounts(base):
    """
    Table representing user accounts in the application.
    """
    __tablename__ = "accounts"

    id = Column(String(length=32), primary_key=True)
    first_name = Column(String(length=32))
    last_name = Column(String(length=32))
    email = Column(String, unique=True)
    hashed_password = Column(String)
    profile_pic_url = Column(String)
    created_at = Column(TIMESTAMP)


base.metadata.create_all(db)
