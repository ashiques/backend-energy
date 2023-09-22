from datetime import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Float, String, Integer, DateTime

from file_ingestion import Base


class EnergyData(Base):
    __tablename__ = "energy_data"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    meter_code: Mapped[str] = Column(String(30))
    serial_number: Mapped[str] = Column(String(30))
    plant_code: Mapped[str] = Column(String(30))
    date_time: Mapped[DateTime] = Column(DateTime, default=datetime.utcnow)
    data_type: Mapped[str] = Column(String(30))
    energy: Mapped[Float] = Column(Float(30))
    units: Mapped[str] = Column(String(30))

    def __repr__(self) -> str:
        return f"EnergyData(id={self.id!r}, name={self.meter_code!r}, fullname={self.serial_number!r})"


class EnergyMaterialView(Base):
    __tablename__ = "energy_data_mv"
    # Define columns that match your materialized view's structure
    meter_code: Mapped[str] = Column(String(30))
    serial_code: Mapped[str] = Column(String(30))
    plant_code: Mapped[str] = Column(String(30))

    # aggregated columns
    max_energy: Mapped[Float] = Column(Float)
    min_energy: Mapped[Float] = Column(Float)
    avg_energy: Mapped[Float] = Column(Float)

    date_time: Mapped[DateTime] = Column(DateTime, default=datetime.utcnow)
