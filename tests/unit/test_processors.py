"""Test file processor data"""
from src.file_processing.processors import LUParser, TOUParser
from datetime import datetime


def test_lu_parser():
    """Test LUParser is working and creating the EnergyData object"""
    data = {
        "MeterPoint Code": "210095893",
        "Serial Number": "210095893",
        "Plant Code": "ED031000001",
        "Date/Time": "31/08/2018 00:45:00",
        "Data Type": "Import Wh Total",
        "Data Value": "0.000000",
        "Units": "kwh",
        "Status": "",
    }
    lu_parsed_data = LUParser(data)
    assert lu_parsed_data.to_model().__str__() == (
        "<EnergyData(id=None, meter_code='210095893', " "serial_number='210095893')>"
    )
    assert lu_parsed_data.to_dict() == {
        "data_type": "Import Wh Total",
        "date_time": datetime(2018, 8, 31, 0, 0),
        "energy": "0.000000",
        "meter_code": "210095893",
        "plant_code": "ED031000001",
        "serial_number": "210095893",
        "status": "",
        "units": "kwh",
    }


def test_tou_parser():
    """Test TOUParser is working and creating the EnergyData object"""
    data = {
        "MeterCode": "212621147",
        "Serial": "212621147",
        "PlantCode": "ED011300245",
        "DateTime": "12/09/2018 5:00",
        "Quality": "A",
        "Stream": "B1",
        "DataType": "Import Wh Total",
        "Energy": "105.6",
        "Units": "kwh",
    }
    tou_parsed_data = TOUParser(data)
    assert tou_parsed_data.to_dict() == {
        "data_type": "Import Wh Total",
        "date_time": datetime(2018, 9, 12, 0, 0),
        "energy": "105.6",
        "meter_code": "212621147",
        "plant_code": "ED011300245",
        "quantity": "A",
        "serial_number": "212621147",
        "stream": "B1",
        "units": "kwh",
    }

    assert tou_parsed_data.to_model().__str__() == (
        "<EnergyData(id=None, meter_code='212621147', " "serial_number='212621147')>"
    )
