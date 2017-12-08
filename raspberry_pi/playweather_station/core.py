from threading import Thread
import time
from datetime import datetime
from pprint import pprint
import requests
import os
import sqlite3
import json


class SensorModule(Thread):
    def __init__(self, name=None, data_collector=None):
        super(SensorModule, self).__init__()
        self.name = name
        self.data_collector = data_collector
        self.running = False

    def start(self):
        self.running = True
        super(SensorModule, self).start()

    def stop(self):
        self.running = False

    def run(self):
        raise NotImplementedError

    def collect(self, value, sub_name=None):
        if self.name and sub_name:
            sensor_name = self.name + '_' + sub_name
        elif sub_name:
            sensor_name = sub_name
        elif self.name:
            sensor_name = self.name
        else:
            sensor_name = None

        if not sensor_name:
            raise ValueError('Can not collect data, a sensor name has not been set')

        self.data_collector.setdefault(sensor_name, []).append({
            'value': value,
            'date': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        })


class PlayWeatherStation:
    def __init__(self, id):
        self.id = id
        self.registered_sensors = {}
        self.data_collector = {}
        self.threads = {}
        self.running = False
        self.delivery_url = 'localhost'
        self.delivery_port = '8000'
        self.db_filename = "pw.sqlite3"
        self.schema_filename = "pw_schema.sql"

    def register(self, sensor_class, name):
        self.registered_sensors[name] = sensor_class(name, self.data_collector)

    def initialize(self):
        self.init_db()
        print("Initializing sensors... ")

        self.running = True
        self.threads = {}
        for sensor_name, sensor in self.registered_sensors.iteritems():
            self.threads[sensor_name] = sensor
            self.threads[sensor_name].start()
            print("=> sensor: '" + sensor_name + "' is running.")

        for _ in range(10):
            time.sleep(5)
            data = {
                "station_id": self.id,
                "location": {
                    "latitude": 19.446264,
                    "longitude": -70.683918,
                    "altitude": 201.45,
                },
                "readings": self.data_collector,
            }
            self.deliver_data(data)
            self.persist_data(data)

            print("*********\n")
            for key, value in self.data_collector.iteritems():
                print("->", key, value)
            for sensor in self.data_collector:
                self.data_collector[sensor] = []
            print("*********\n\n")

    def stop(self):
        print("Wating for all systems to shutdown")
        self.running = False
        for thread in self.threads.values():
            thread.stop()
            thread.join()

        print("Shutdown successful")

    def deliver_data(self, data):
        print("\n\n\nsending:")
        print(json.dumps(data))
        print("\n to:",
              'http://{url}:{port}/api/sensor_readings_bundle/new/'.format(
                  url=self.delivery_url,
                  port=self.delivery_port
              ))

        requests.post(
            'http://{url}:{port}/api/sensor_readings_bundle/new/'.format(
                url=self.delivery_url,
                port=self.delivery_port
            ),
            data=json.dumps(data)
        )

    def init_db(self):
        if not os.path.exists(self.db_filename):
            with sqlite3.connect(self.db_filename) as conn:
                print('Creating schema')
                with open(self.schema_filename, 'rt') as f:
                    schema = f.read()
                conn.executescript(schema)
                print('Schema created\n\n')
        else:
            print("Database already created")

    def persist_data(self, data):
        if os.path.exists(self.db_filename):
            print("Persisting data")
            with sqlite3.connect(self.db_filename) as conn:
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
