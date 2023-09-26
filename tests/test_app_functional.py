from src.app import app


def test_home_page():
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b"Root Loaded \n" in response.data


def test_load_data():
    with app.test_client() as test_client:
        response = test_client.get('/load-data')
        assert response.status_code == 200
        assert b'{"message":"Load data complete"}\n' in response.data


def test_populate_view():
    with app.test_client() as test_client:
        response = test_client.get('/populate-view')
        assert response.status_code == 200
        assert b'{"message":"Load data in view complete"}\n' in response.data


def test_get_data_success():
    with app.test_client() as test_client:
        data = {
            'meter_code': '210095893',
            'date_time': '01/09/2015',
            'serial_code': '210095893'
        }
        response = test_client.get('/get-data', query_string=data)
        assert response.status_code == 200
        assert (b'{"avg_energy":1.7166666666666668,"date_time":"Tue, 01 Sep 2015 00:00:00 GMT","id":5,'
                b'"max_energy":4.2,"meter_code":"210095893","min_energy":0.0,"plant_code":"ED031000001",'
                b'"serial_code":"210095893"}\n') in response.data


def test_get_data_date_validation():
    with app.test_client() as test_client:
        data = {
            'meter_code': '210095893',
            'date_time': '01/09/201',
            'serial_code': '210095893'
        }
        response = test_client.get('/get-data', query_string=data)
        assert response.status_code == 400
        assert (b'<!doctype html>\n<html lang=en>\n<title>400 Bad Request</title>\n<h1>Bad Request</h1>\n<p>date_time '
                b'should in %d/%m/%Y</p>\n') in response.data


def test_get_data_meter_code_validation():
    with app.test_client() as test_client:
        data = {
            'meter_code': '',
            'date_time': '01/09/2015',
            'serial_code': '210095893'
        }
        response = test_client.get('/get-data', query_string=data)
        assert response.status_code == 400
        assert (
                   b'<!doctype html>\n<html lang=en>\n<title>400 Bad Request</title>\n<h1>Bad '
                   b'Request</h1>\n<p>meter_code is mandatory</p>\n') in response.data


def test_get_data_serial_code_validation():
    with app.test_client() as test_client:
        data = {
            'meter_code': '210095893',
            'date_time': '01/09/2015',
            'serial_code': ''
        }
        response = test_client.get('/get-data', query_string=data)
        assert response.status_code == 400
        assert (b'<!doctype html>\n<html lang=en>\n<title>400 Bad Request</title>\n<h1>Bad '
                b'Request</h1>\n<p>serial_code is mandatory</p>\n') in response.data


def test_get_data_no_data():
    with app.test_client() as test_client:
        data = {
            'meter_code': '210095893',
            'date_time': '01/09/2015',
            'serial_code': '210095892'
        }
        response = test_client.get('/get-data', query_string=data)
        assert response.status_code == 200
        assert b'{"message":"energy data not present"}\n' in response.data
