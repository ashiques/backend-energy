from flask import Flask

from file_ingestion import load_tables
from file_processing import handle_different_file

app = Flask(__name__)
load_tables()


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/load-data")
def add_user():
    handle_different_file()
    return "Process complete"


@app.route("/users")
def get_users():
    return "Get all Users"


if __name__ == "__main__":
    app.run()
