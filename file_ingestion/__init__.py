from sqlalchemy.orm import DeclarativeBase
import sqlalchemy as db

CONNECTION_URL = "postgresql://postgres:example@localhost/postgres"
SQL_LITE = "sqlite:///data/test.db"
engine = db.create_engine(CONNECTION_URL)


class Base(DeclarativeBase):
    pass


def load_tables():
    Base.metadata.create_all(engine)
