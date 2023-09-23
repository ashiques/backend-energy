from enum import Enum

from pathlib import Path
from os import listdir
import csv
from typing import AnyStr

from sqlalchemy.orm import Session

from file_ingestion import engine
from file_ingestion.models import aggregate_energy_data, get_energy_data
from file_processing.processors import LUParser, Parser, TOUParser
from file_ingestion import Dialects

from datetime import datetime

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
    data = (
        [LUParser(row).to_model() for row in reader]
        if file_type == FileType.LU
        else [TOUParser(row).to_model() for row in reader]
    )
    print(f"Count of entities loaded: {len(data)}")
    session.add_all(data)
    session.commit()


def handle_files_load():
    for path in get_file_path():
        print(f"Process  file: {path.name}")
        with open(path) as file_name:
            reader = csv.DictReader(file_name)
            if path.name.startswith("LP_"):
                # handle for LP files
                _load_data(reader, FileType.LU)
            elif path.name.startswith("TOU_"):
                # handle for TOU files
                _load_data(reader, FileType.TOU)


def aggregate(dialect: Dialects):
    aggregate_energy_data(dialect)


def get_data(meter_code: AnyStr, serial_code: AnyStr, date_time: datetime):
    return get_energy_data(meter_code, serial_code, date_time)
