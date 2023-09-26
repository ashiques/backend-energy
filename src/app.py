from datetime import datetime
from flask import Flask, jsonify, request, abort
from typing import AnyStr

from .file_ingestion import load_tables
from .file_processing import handle_files_load, aggregate, get_data
from .file_processing.processors import DATE_FORMAT

app = Flask(__name__)
# reload on application re-load
load_tables()


def is_valid_datetime(string):
    try:
        datetime.strptime(string, DATE_FORMAT)
        return True
    except ValueError:
        return False


@app.route("/")
def root():
    return "Root Loaded \n"


@app.route("/load-data", methods=["GET"])
def load_data():
    # re-load tables to maintain the view
    load_tables()
    handle_files_load()
    return jsonify({"message": "Load data complete"})


@app.route("/populate-view", methods=["GET"])
def load_energy_info():
    aggregate()
    return jsonify({"message": "Load data in view complete"})


@app.route("/get-data", methods=["GET"])
def fetch_energy_data():
    if not request.args.get("date_time") or not is_valid_datetime(
        request.args.get("date_time")
    ):
        abort(400, f"date_time should in {DATE_FORMAT}")

    if not request.args.get("meter_code"):
        abort(400, "meter_code is mandatory")

    if not request.args.get("serial_code"):
        abort(400, "serial_code is mandatory")

    meter_code: AnyStr = request.args.get("meter_code")
    serial_code: AnyStr = request.args.get(
        "serial_code",
    )
    date_time: datetime = datetime.strptime(
        request.args.get("date_time", "date_time not provided"), DATE_FORMAT
    )
    energy_data = get_data(meter_code, serial_code, date_time)

    return (
        jsonify(energy_data)
        if energy_data
        else jsonify({"message": "energy data not present"})
    )


if __name__ == "__main__":
    app.run()
