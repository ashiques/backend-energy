"""Test for functional changes"""
from src.app import app


# Pre-requisite, db connection string has to be updated with the detail from local postgres created from docker compose
# These tests expect the local postgres DB to be started from the config in docker-compose.yml


def test_home_page():
    """Test to check if the root endpoint is loaded"""
    with app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200
        assert b"Root Loaded \n" in response.data


def test_load_data():
    """Test to check if the load-data endpoint is up and working"""
    with app.test_client() as test_client:
        response = test_client.get("/load-data")
        assert response.status_code == 200
        assert b'{"message":"Load data complete"}\n' in response.data


def test_populate_view():
    """Test to check if the populate-view endpoint is up and working"""
    with app.test_client() as test_client:
        response = test_client.get("/populate-view")
        assert response.status_code == 200
        assert b'{"message":"Load data in view complete"}\n' in response.data


def test_get_data_success():
    """Test to check if the get-data endpoint with parameters is up and working"""
    with app.test_client() as test_client:
        data = {
            "meter_code": "210095893",
            "date_time": "01/09/2015",
            "serial_code": "210095893",
        }
        response = test_client.get("/get-data", query_string=data)
        assert response.status_code == 200
        assert (
            b'{"avg_energy":1.7166666666666668,"date_time":"Tue, 01 Sep 2015 00:00:00 GMT","id":5,'
            b'"max_energy":4.2,"meter_code":"210095893","min_energy":0.0,"plant_code":"ED031000001",'
            b'"serial_code":"210095893"}\n'
        ) in response.data


def test_get_data_date_validation():
    """Test to check if the get-data endpoint with parameters fail for validation error of date"""
    with app.test_client() as test_client:
        data = {
            "meter_code": "210095893",
            "date_time": "01/09/201",
            "serial_code": "210095893",
        }
        response = test_client.get("/get-data", query_string=data)
        assert response.status_code == 400
        assert (
            b"<!doctype html>\n<html lang=en>\n<title>400 Bad Request</title>\n<h1>Bad Re"
            b"quest</h1>\n<p>date_time should be in %d/%m/%Y</p>\n"
        ) in response.data


def test_get_data_meter_code_validation():
    """Test to check if the get-data endpoint with parameters fail for validation error of meter_code"""
    with app.test_client() as test_client:
        data = {"meter_code": "", "date_time": "01/09/2015", "serial_code": "210095893"}
        response = test_client.get("/get-data", query_string=data)
        assert response.status_code == 400
        assert (
            b"<!doctype html>\n<html lang=en>\n<title>400 Bad Request</title>\n<h1>Bad "
            b"Request</h1>\n<p>meter_code is mandatory</p>\n"
        ) in response.data


def test_get_data_serial_code_validation():
    """Test to check if the get-data endpoint with parameters fail for validation error of serial_code"""
    with app.test_client() as test_client:
        data = {"meter_code": "210095893", "date_time": "01/09/2015", "serial_code": ""}
        response = test_client.get("/get-data", query_string=data)
        assert response.status_code == 400
        assert (
            b"<!doctype html>\n<html lang=en>\n<title>400 Bad Request</title>\n<h1>Bad "
            b"Request</h1>\n<p>serial_code is mandatory</p>\n"
        ) in response.data


def test_get_data_no_data():
    """Test to check if the get-data endpoint with parameters return message when not data retrieved"""
    # If data load has not worked in the previous steps then this endpoint will always give this response.
    with app.test_client() as test_client:
        data = {
            "meter_code": "210095893",
            "date_time": "01/09/2015",
            "serial_code": "210095892",
        }
        response = test_client.get("/get-data", query_string=data)
        assert response.status_code == 200
        assert b'{"message":"energy data not present"}\n' in response.data
