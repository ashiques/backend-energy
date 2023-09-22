from typing import AnyStr, Dict

from file_ingestion.models import EnergyData


class FileRow:
    def __init__(
        self, meter_code, serial_number, plant_code, date_time, data_type, energy, units
    ):
        self.meter_code = meter_code
        self.serial_number = serial_number
        self.plant_code = plant_code
        self.date_time = date_time
        self.date_type = data_type
        self.energy = energy
        self.units = units

    def __str__(self):
        return """<FileRow meter_code:<{}> serial_number:<{}>>""".format(
            self.meter_code, self.serial_number
        )


class LUParser:
    def __init__(self, data: Dict):
        self.data = data

    @property
    def meter_code(self) -> AnyStr:
        return self.data["MeterPoint Code"]

    @property
    def serial_number(self) -> AnyStr:
        return self.data["Serial Number"]

    @property
    def plant_code(self) -> AnyStr:
        return self.data["Plant Code"]

    @property
    def date_time(self) -> AnyStr:
        return self.data["Date/Time"]

    @property
    def data_type(self) -> AnyStr:
        return self.data["Data Type"]

    @property
    def energy(self) -> AnyStr:
        return self.data["Data Value"]

    @property
    def units(self) -> AnyStr:
        return self.data["Units"]

    @property
    def status(self) -> AnyStr:
        return self.data["Status"]

    def convert_to_model(self) -> EnergyData:
        return EnergyData(
            id=None,
            meter_code=self.meter_code,
            serial_number=self.serial_number,
            plant_code=self.plant_code,
            date_time=self.date_time,
            data_type=self.data_type,
            energy=self.energy,
            units=self.units,
        )
