from pathlib import Path
from os import listdir
import csv

from sqlalchemy.orm import Session

from file_ingestion import engine
from file_processing.processors import LUParser

file_path = Path(__file__).parents[1].joinpath("datafiles")


def get_file_path():
    return [
        file_path.joinpath(file_name)
        for file_name in listdir(file_path)
        if file_path.joinpath(file_name).is_file()
    ]


def read_files(path: Path):
    with open(path) as file_name:
        reader = csv.DictReader(file_name)
        session = Session(engine)
        for row in reader:
            session.add(LUParser(row).convert_to_model())
        session.commit()


def handle_different_file():
    for path in get_file_path():
        if path.name.startswith("LP_"):
            read_files(path)
            # handle for LP files
            pass
        elif path.name.startswith("TOU_"):
            # handle for TOU files
            pass
