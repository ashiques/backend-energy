import datetime

from src.file_ingestion.models import EnergyMaterialView, EnergyData
from datetime import datetime
from src.app import DATE_FORMAT


def test_energy_data_model():
    """
    Testing to validate if EnergyData object is created properly
    """
    energy_obj = EnergyData(
        meter_code="test_meter",
        serial_number="test_serial",
        plant_code="test_plant",
        date_time=datetime.strptime("01/08/2020", DATE_FORMAT),
        data_type="test_data_type",
        energy=16.6,
        units="kwh",
    )
    assert (
        energy_obj.__repr__()
        == "<EnergyData(id=None, meter_code='test_meter', serial_number='test_serial')>"
    )
    assert energy_obj.units == "kwh"
    assert energy_obj.plant_code == "test_plant"
    assert energy_obj.data_type == "test_data_type"
    assert energy_obj.energy == 16.6


def test_energy_material_view_model():
    """
    Testing to validate if EnergyMaterialView object is created properly
    """
    energy_material_obj = EnergyMaterialView(
        meter_code="test_meter",
        serial_code="test_serial",
        plant_code="test_plant",
        date_time=datetime.strptime("01/08/2020", DATE_FORMAT),
        max_energy=11.4,
        min_energy=5.0,
        avg_energy=7.5,
    )
    assert energy_material_obj.__repr__() == (
        "<EnergyMaterialView(id=None, meter_code='test_meter', "
        "serial_code='test_serial')>"
    )

    assert energy_material_obj.to_dict() == {
        "avg_energy": 7.5,
        "date_time": datetime(2020, 8, 1, 0, 0),
        "id": None,
        "max_energy": 11.4,
        "meter_code": "test_meter",
        "min_energy": 5.0,
        "plant_code": "test_plant",
        "serial_code": "test_serial",
    }
