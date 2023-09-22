from enum import Enum

from pathlib import Path
from os import listdir
import csv

from sqlalchemy.orm import Session

from file_ingestion import engine
from file_processing.processors import LUParser, Parser, TOUParser

file_path = Path(__file__).parents[1].joinpath("datafiles")


class FileType(Enum):
    LU = "LU"
    TOU = "TOU"


def get_file_path():
    return [
        file_path.joinpath(file_name)
        for file_name in listdir(file_path)
        if file_path.joinpath(file_name).is_file()
    ]


def _load_data(reader, file_type: FileType):
    session = Session(engine)
    data = [LUParser(row).convert_to_model() for row in reader] if file_type == FileType.LU else [
        TOUParser(row).convert_to_model() for row in reader]
    print("Count of entities loaded: {}".format(len(data)))
    session.add_all(data)
    session.commit()


def handle_different_file():
    for path in get_file_path():
        print("inside process {}".format(path.name))
        with open(path) as file_name:
            reader = csv.DictReader(file_name)
            if path.name.startswith("LP_"):
                _load_data(reader, FileType.LU)
                # handle for LP files
                pass
            elif path.name.startswith("TOU_"):
                # handle for TOU files
                _load_data(reader, FileType.TOU)
