"""This module is to handle the file processing"""
from enum import Enum

from pathlib import Path
from os import listdir
import csv
from typing import AnyStr, Optional, Dict

from sqlalchemy.orm import Session

from ..file_ingestion import engine
from ..file_ingestion.models import aggregate_energy_data, get_energy_data
from ..file_processing.processors import LUParser, TOUParser

from datetime import datetime

# path of the datafiles, needs to be changes if required
file_path = Path(__file__).parents[1].joinpath("datafiles")


class FileType(Enum):
    """Enum for filetypes"""

    LU = "LU"
    TOU = "TOU"


def get_file_path():
    """Get all the full file names from a path"""
    return [
        file_path.joinpath(file_name)
        for file_name in listdir(file_path)
        if file_path.joinpath(file_name).is_file()
    ]


def _load_data(reader, file_type: FileType):
    """Process function to load the data from files to DB"""
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
    """
    Function to handle file path fetch and read
    :return: None
    """
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


def aggregate():
    """Aggregate the energy data by running the aggregation query"""
    aggregate_energy_data()


def get_data(
    meter_code: AnyStr, serial_code: AnyStr, date_time: datetime
) -> Optional[Dict]:
    """
    Get the energy data matching the parameter from view table.
    :param meter_code: meter_code parameter
    :param serial_code: serial parameter
    :param date_time: date_time parameter
    :return: Option]
    """
    return get_energy_data(meter_code, serial_code, date_time)
