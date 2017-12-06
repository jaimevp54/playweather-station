import requests
import random
from datetime import datetime
from requests import ConnectionError
import time

import json
import sqlite3
import os


def send_data(data, host="localhost", port="8000", path="api/sensor_readings_bundle/new/"):
    try:
        print("sending data to http://{host}:{port}/{path}".format(host=host, port=port, path=path))

        response = requests.post("http://{host}:{port}/{path}".format(host=host, port=port, path=path),
                                 data=json.dumps(data))
        if response.status_code == 200:
            print(response.text)
        else:
            print(response)
    except ConnectionError as e:
        print("error:" + str(e) + "\n\n")


db_filename = "pw.sqlite3"
schema_filename = "pw_schema.sql"


def init_db():
    if not os.path.exists(db_filename):
        with sqlite3.connect(db_filename) as conn:
            print('Creating schema')
            with open(schema_filename, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)
            print('Schema created\n\n')
    else:
        print("Database already created")


def persist_data(data):
    if os.path.exists(db_filename):
        print("Persisting data")
        with sqlite3.connect(db_filename) as conn:
            # c = conn.cursor()
            for sensor, readings in data['readings'].items():
                for reading in readings:
                    conn.execute(
                        """
                        INSERT INTO readings (sensor, value, reading_date)
                        VALUES (?,?,?) 
                        """, (sensor, reading['value'], datetime.strptime(reading['date'], '%Y-%m-%dT%H:%M:%SZ'))
                    )
            conn.commit()
        print("Done: Data persisted")
    else:
        print("Database still not created. Run init_db() before being able to persiste data")


init_db()
while True:
    time.sleep(5)
    pw1 = {
        "station_id": "pw1",
        "location": {
            "latitude": 19.446264,
            "longitude": -70.683918,
            "altitude": 201.45,
        },
        "readings": {
            "pw1_s1": [
                {"value": random.randrange(100, 120), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
            "pw1_s2": [
                {"value": random.randrange(100, 1200), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
            "pw1_s3": [
                {"value": random.randrange(10, 19), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
            "pw1_s4": [
                {"value": random.randrange(70, 120), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
        }
    }

    persist_data(pw1)
    send_data(pw1)

    pw2 = {
        "station_id": "pw2",
        "location": {
            "latitude": 19.446359,
            "longitude": -70.683111,
            "altitude": 102.45,
        },
        "readings": {
            "pw2_s1": [
                {"value": random.randrange(200, 220), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
            "pw2_s2": [
                {"value": random.randrange(80, 1000), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
            "pw2_s3": [
                {"value": random.randrange(53, 62), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
            "pw2_s4": [
                {"value": random.randrange(113, 163), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
            "pw2_s5": [
                {"value": random.randrange(43, 163), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
        }
    }
    send_data(pw2)

    pw3 = {
        "station_id": "pw3",
        "location": {
            "latitude": 19.446415,
            "longitude": -70.684023,
            "altitude": 201.87,
        },
        "readings": {
            "pw3_s1": [
                {"value": random.randrange(68, 88), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
            "pw3_s2": [
                {"value": random.randrange(1430, 1630), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
            "pw3_s3": [
                {"value": random.randrange(10, 62), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
            "pw3_s4": [
                {"value": random.randrange(113, 206), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
            "pw3_s5": [
                {"value": random.randrange(83, 175), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
            "pw3_s6": [
                {"value": random.randrange(53, 146), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
        }
    }
    send_data(pw3)
