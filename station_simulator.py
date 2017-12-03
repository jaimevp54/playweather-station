import requests
import random
from datetime import datetime
from requests import ConnectionError

import json


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


while True:
    time.sleep(5)
    pw1 = {
        "station_id": "pw1",
        "location": {
            "longitude": 19.446264,
            "latitude": -70.683918,
            "altitude": 201.45,
        },
        "readings": {
            "pw1_s1": [
                {"value": random.randrange(100, 120), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
            "pw1_s2": [
                {"value": random.randrange(1000, 1200), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
            "pw1_s3": [
                {"value": random.randrange(10, 19), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
            "pw1_s4": [
                {"value": random.randrange(70, 120), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
        }
    }

    send_data(pw1)

    pw2 = {
        "station_id": "pw2",
        "location": {
            "longitude": 19.446359,
            "latitude": -70.683111,
            "altitude": 102.45,
        },
        "readings": {
            "pw2_s1": [
                {"value": random.randrange(200, 220), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
            ],
            "pw2_s2": [
                {"value": random.randrange(800, 1000), "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')},
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
            "longitude": 19.446415,
            "latitude": -70.684023,
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
