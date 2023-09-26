"""
All the models and database processing expected to be done as part of the build
"""
from typing import AnyStr, Optional, Dict

from sqlalchemy.orm import Mapped, Session
from sqlalchemy import Column, Float, String, Integer, DateTime
from sqlalchemy.sql import func, text

from ..file_ingestion import Base, engine
from datetime import datetime


class EnergyData(Base):
    """
    Table to store the information of Energy Data from file
    """

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
        return f"<EnergyData(id={self.id!r}, meter_code={self.meter_code!r}, serial_number={self.serial_number!r})>"


class EnergyMaterialView(Base):
    """
    View table to load the data from the aggregation activity
    """

    __tablename__ = "energy_data_view"
    # Define columns for the view table
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    meter_code: Mapped[str] = Column(String(30))
    serial_code: Mapped[str] = Column(String(30))
    plant_code: Mapped[str] = Column(String(30))

    # aggregated columns
    max_energy: Mapped[Float] = Column(Float)
    min_energy: Mapped[Float] = Column(Float)
    avg_energy: Mapped[Float] = Column(Float)

    date_time: Mapped[DateTime] = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "meter_code": self.meter_code,
            "serial_code": self.serial_code,
            "plant_code": self.plant_code,
            "max_energy": self.max_energy,
            "min_energy": self.min_energy,
            "avg_energy": self.avg_energy,
            "date_time": self.date_time,
        }

    def __repr__(self):
        return f"<EnergyMaterialView(id={self.id!r}, meter_code={self.meter_code!r}, serial_code={self.serial_code!r})>"


def aggregate_energy_data() -> None:
    """
    Aggregation processing function to read data from energy data table
    and run aggregate query to be stored in the view table.

    :return: None
    """
    session = Session(engine)

    query = session.query(
        EnergyData.meter_code,
        EnergyData.serial_number,
        EnergyData.plant_code,
        func.max(EnergyData.energy).label("max_energy"),
        func.min(EnergyData.energy).label("min_energy"),
        func.avg(EnergyData.energy).label("avg_energy"),
        EnergyData.date_time,
    ).group_by(
        EnergyData.meter_code,
        EnergyData.serial_number,
        EnergyData.plant_code,
        EnergyData.date_time,
    )
    # query the results
    results = query.all()
    if len(results) != 0:
        # clean up the table
        truncate_query = f"TRUNCATE TABLE {EnergyMaterialView.__tablename__}"

        session.execute(text(truncate_query))
        session.commit()

        # create the models
        view_objs = [
            EnergyMaterialView(
                meter_code=row[0],
                serial_code=row[1],
                plant_code=row[2],
                max_energy=row[3],
                min_energy=row[4],
                avg_energy=row[5],
                date_time=row[6],
            )
            for row in query.all()
        ]
        # store the models in db
        session.add_all(view_objs)
        session.commit()

    session.close()


def get_energy_data(
    meter_code: AnyStr, serial_code: AnyStr, date_time: datetime
) -> Optional[Dict]:
    """
    Get the data stored in view table for get-data query
    :param meter_code: meter_code parameter
    :type : AnyStr
    :param serial_code: serial_code parameter
    :type : AnyStr
    :param date_time: date_time parameter
    :return: Optional[Dict]
    """
    session = Session(engine)
    energy_data: Optional[EnergyMaterialView] = (
        session.query(EnergyMaterialView)
        .filter(
            EnergyMaterialView.meter_code == meter_code,
            EnergyMaterialView.serial_code == serial_code,
            EnergyMaterialView.date_time == date_time,
        )
        .first()
    )
    session.close()
    return energy_data.to_dict() if energy_data else None
