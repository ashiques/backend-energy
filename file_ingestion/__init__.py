from sqlalchemy.orm import DeclarativeBase
import sqlalchemy as db
from enum import Enum

CONNECTION_URL = "postgresql://postgres:example@localhost/postgres"
CONNECTION_SQLITE = "sqlite:///data/test.db"
engine = db.create_engine(CONNECTION_SQLITE)


class Dialects(Enum):
    SQLITE = "SQLITE"
    PG = "PG"


class Base(DeclarativeBase):
    pass


def load_tables():
    # drop all tables
    Base.metadata.drop_all(engine)
    # re-create all the tables
    Base.metadata.create_all(engine)
