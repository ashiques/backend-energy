from flask import Flask

from file_ingestion import load_tables
from file_processing import handle_files_load

app = Flask(__name__)
load_tables()


@app.route("/")
def root():
    return "Hello, World!"


@app.route("/load-data")
def load_data():
    handle_files_load()
    return "Process complete"


@app.route("/get-data")
def fetch_energy_data():
    return "Get energy data"


if __name__ == "__main__":
    app.run()
