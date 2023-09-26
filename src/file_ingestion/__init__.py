"""
Init file to load the tables and create SQLAlchemy Engine,
"""
from sqlalchemy.orm import DeclarativeBase
import sqlalchemy as db
from os import environ

engine = db.create_engine(environ["DB_URL"])


class Base(DeclarativeBase):
    """
    Supporting class for Base and table creations
    """

    pass


def load_tables():
    """
    Function to drop and re-create all the registered tables
    :return:
    """
    # drop all tables
    Base.metadata.drop_all(engine)
    # re-create all the tables
    Base.metadata.create_all(engine)
