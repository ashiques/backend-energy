from abc import ABC, abstractmethod
from typing import AnyStr, Dict

from datetime import datetime

from ..file_ingestion.models import EnergyData

DATE_FORMAT = "%d/%m/%Y"


class Parser(ABC):

    def __init__(self, data: Dict):
        self.data = data

    @property
    @abstractmethod
    def meter_code(self) -> AnyStr:
        pass

    @property
    @abstractmethod
    def serial_number(self) -> AnyStr:
        pass

    @property
    @abstractmethod
    def plant_code(self) -> AnyStr:
        pass

    @property
    @abstractmethod
    def date_time(self) -> AnyStr:
        pass

    @property
    @abstractmethod
    def data_type(self) -> AnyStr:
        pass

    @property
    @abstractmethod
    def energy(self) -> AnyStr:
        pass

    @property
    @abstractmethod
    def units(self) -> AnyStr:
        pass

    def to_model(self) -> EnergyData:
        return EnergyData(
            meter_code=self.meter_code,
            serial_number=self.serial_number,
            plant_code=self.plant_code,
            date_time=self.date_time,
            data_type=self.data_type,
            energy=self.energy,
            units=self.units,
        )


class LUParser(Parser, ABC):
    def __init__(self, data: Dict):
        super().__init__(data)

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
    def date_time(self) -> datetime:
        return datetime.strptime(self.data["Date/Time"][:10], DATE_FORMAT)

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


class TOUParser(Parser, ABC):

    def __init__(self, data: Dict):
        super().__init__(data)

    @property
    def meter_code(self) -> AnyStr:
        return self.data["MeterCode"]

    @property
    def serial_number(self) -> AnyStr:
        return self.data["Serial"]

    @property
    def plant_code(self) -> AnyStr:
        return self.data["PlantCode"]

    @property
    def date_time(self) -> datetime:
        return datetime.strptime(self.data["DateTime"][:10], DATE_FORMAT)

    @property
    def quantity(self):
        return self.data["Quality"]

    @property
    def stream(self):
        return self.data["Stream"]

    @property
    def data_type(self) -> AnyStr:
        return self.data["DataType"]

    @property
    def energy(self) -> AnyStr:
        return self.data["Energy"]

    @property
    def units(self) -> AnyStr:
        return self.data["Units"]
