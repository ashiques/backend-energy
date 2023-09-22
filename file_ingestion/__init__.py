from sqlalchemy.orm import DeclarativeBase
import sqlalchemy as db

engine = db.create_engine("sqlite:///data/test.db")


class Base(DeclarativeBase):
    pass


def load_tables():
    Base.metadata.create_all(engine)
