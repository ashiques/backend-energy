from sqlalchemy.orm import DeclarativeBase
import sqlalchemy as db
from os import environ

engine = db.create_engine(environ["DB_URL"])


class Base(DeclarativeBase):
    pass


def load_tables():
    # drop all tables
    Base.metadata.drop_all(engine)
    # re-create all the tables
    Base.metadata.create_all(engine)
