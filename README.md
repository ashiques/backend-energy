# Backend Energy API for handling LP and TOU file ingestion

---
This is a sample application created with Flask and SQLAlchemy to interact with LP and TOU energy file data.

Below are the following functionalities expected:

* Load the data from files to DB, using the ORM
* Populate a view table with the aggregated query for *MIN*, *MAX* and *AVG* operations.
* Exhibit and API end-point to fetch the aggregated data from table.

As part of the modelling of the tables and queries following assumptions are made

## Assumptions

* Load data can be re-run many times so, tables are re-created for each run.
* When the app gets re-loaded each time also the tables are re-loaded
* There is an order of execution for apis from end-point which needs to be followed to see the data.
* Expecting the files to be either LP or TOU format
* Expect energy units to be the same, since conversion logic between each is not implemented.
* date time data provided is expected to be in `%d/%m/%Y` format, so slicing is done from the datatime field in input.

---

## Database Modelling

### Connection Information:

The connection details can be changed depending up on the use case, but be mindful that it needs to be changed in
both `Dockerfile` and `docker-compose.yml`

```yaml
    environment:
      POSTGRES_PASSWORD: example
      POSTGRES_USER: postgres
```

```DB_URL: postgresql://postgres:example@db/postgres```

### Energy Data Table

Table to load all the data parsed from the files.

![img.png](imgs/img.png)

### Energy Data View Table

Table to store the data aggregated from energy_data, included the query to populate the table.

![img_1.png](imgs/img_1.png)

```postgresql
SELECT METER_CODE,
       SERIAL_NUMBER,
       MAX(ENERGY) AS MAX_ENERGY,
       MIN(ENERGY) AS MIN_ENERGY,
       AVG(ENERGY) AS AVG_ENERGY,
       DATE_TIME
FROM ENERGY_DATA
GROUP BY METER_CODE,
         SERIAL_NUMBER,
         DATE_TIME;

```

---

## APIs and Usage

The expectation is the endpoints needs to be called in order,
The order of execution is as follows:

* `/load-data` for loading the data from datafiles folder.
* `/populate-view` for loading the view table with the aggregate from the energy data table.
* `/get-data` with parameters *meter_code*,*serial_code*, *date_time*

### Load the data with the endpoint:

```bash
curl --location 'http://localhost:8080/load-data'
```

### Aggregate the data into view table:

```bash
curl --location 'http://localhost:8080/populate-view'
```

### Query the view table with parameters

#### Request format

```bash
curl --location 'http://localhost:8080/get-data?meter_code=210095893&date_time=01%2F09%2F2015&serial_code=210095893'
```

#### Response format

##### Sample Success

```json
{
  "message": "energy data not present"
}
```

#### Sample No Data:

```json
{
  "avg_energy": 1.7166666666666668,
  "date_time": "Tue, 01 Sep 2015 00:00:00 GMT",
  "id": 5,
  "max_energy": 4.2,
  "meter_code": "210095893",
  "min_energy": 0.0,
  "plant_code": "ED031000001",
  "serial_code": "210095893"
}
```

#### Sample input validations:

```html

<!doctype html>
<html lang=en>
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>date_time should in %d/%m/%Y</p>
```

---

## Nuances of the implementation:

* If connection information are changed it needs to be changes in the Dockerfile and docker-compose.yml.
* Have not implemented the change from wsgi to gunicorn for production server implementation.




