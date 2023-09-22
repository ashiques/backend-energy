from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Float, String, Integer

from file_ingestion import Base


class EnergyData(Base):
    __tablename__ = "energy_data"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    meter_code: Mapped[str] = Column(String(30))
    serial_number: Mapped[str] = Column(String(30))
    plant_code: Mapped[str] = Column(String(30))
    date_time: Mapped[str] = Column(String(30))
    data_type: Mapped[str] = Column(String(30))
    energy: Mapped[Float] = Column(Float(30))
    units: Mapped[str] = Column(String(30))

    def __repr__(self) -> str:
        return f"EnergyData(id={self.id!r}, name={self.meter_code!r}, fullname={self.serial_number!r})"
