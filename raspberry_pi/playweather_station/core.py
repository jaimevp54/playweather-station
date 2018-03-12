from threading import Thread
from playweather_station.sensors.gps import GPS
import time
from datetime import datetime
from pprint import pprint
import requests
import os
import sqlite3
import json
from pprint import pprint
import json


class SensorModule(Thread):
    """Sensor Module base class, all sensors to be integrated with the system must subclass this"""

    def __init__(self, name=None, data_collector=None, collection_interval=30):
        super(SensorModule, self).__init__()
        self.name = name
        self.data_collector = data_collector
        self.collection_interval = int(collection_interval)
        self.running = False
        self.setup_vars = {}

    def start(self):
        self.running = True
        super(SensorModule, self).start()

    def stop(self):
        self.running = False

    def setup(self):
        pass

    def capture_single_data(self):
        """ 
        Capture a single reading from the senser
        MUST be implemented by each module.
        """
        raise NotImplementedError

    def run(self):
        """
        Run sensor module main loop, which will continue until the station's main thread is stopped.
        """
        print('Setting up sensor: ' + self.name)
        self.setup()
        while self.running:
            time.sleep(self.collection_interval)
            captured_data = self.capture_single_data()
            self.collect(captured_data)

        self.cleanup()

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
    def __init__(self):
        self.id = "not-set"
        self.registered_sensors = {}
        self.data_collector = {}
        self.delivery_interval = 10
        self.threads = {}
        self.running = False
        self.delivery_url = 'https://playweather-pucmm.herokuapp.com'  # TODO turn this into a constant
        self.delivery_port = '8000'  # TODO turn this into a constant
        self.db_filename = "pw.sqlite3"  # TODO turn this into a constant
        self.schema_filename = "pw_schema.sql"  # TODO turn this into a constant

    def register(self, sensor_class, name=""):
        if not name:
            name = "sensor" + str(
                len(self.registered_sensors))  # TODO make sure these names are not possible to be repeated

        try:
            self.registered_sensors[name] = sensor_class(name, self.data_collector, collection_interval=2)
        except Exception as e:
            print("Error while trying to register module '{}':\n {}".format(name, e.message))

    def initialize(self, config, gps_on=True):
        # set configuration parameters
        self.config = config
        self.id = config['PLAYWEATHER_STATION']['id']
        self.delivery_interval = int(config['PLAYWEATHER_STATION']['delivery_interval'])

        for sensor_name, sensor in self.registered_sensors.iteritems():
            try:
                sensor.collection_interval = int(config[sensor_name.upper()]['collection_interval'])
            except Exception as e:
                print(sensor_name + " found in config was not installed? e:" + e.message)

        # initialize database
        self.init_db()

        print("Initializing GPS... ")
        self.gps = GPS()

        print("Initializing sensors... ")
        self.running = True
        self.threads = {}

        for sensor_name, sensor in self.registered_sensors.iteritems():
            self.threads[sensor_name] = sensor
            self.threads[sensor_name].start()
            print("=> sensor: '" + sensor_name + "' is running.")
        pprint("Running with the following configs:" )

        for section in self.config.sections():
            print(section + ": ")

            print(dict(self.config.items(section)))

        while True:
            print(str(self.delivery_interval)+ "????")
            
            time.sleep(self.delivery_interval)
            data = {
                "station_id": self.id,
                "location": self.get_current_location(),
                "readings": self.data_collector,
            }

            # is_delivered = self.deliver_data(data)
            # self.persist_data(data, is_delivered)

            self.send_undelivered_data()

            for sensor in self.data_collector:
                self.data_collector[sensor] = []

            #  print("*********\n")
            #  for key, value in self.data_collector.iteritems():
            #      print("->", key, value)
            #  for sensor in self.data_collector:
            #      self.data_collector[sensor] = []
            #  print("*********\n\n")

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
        # print("\n to:",
        #       'http://{url}:{port}/api/sensor_readings_bundle/new/'.format(
        #           url=self.delivery_url,
        #           port=self.delivery_port
        #       ))

        response = requests.post(
            '{url}/api/sensor_readings_bundle/new/'.format(
                url=self.delivery_url,
            ),
            data=json.dumps(data)
        )

        if False and response.status_code == 200:
            print(response.text)
            return True
        else:
            print(response)
            return False

    def get_current_location(self):
        # self.gps.read()

        location = {}
        #if self.gps.fix !=0:
        if False:
            location = {
                "latitude": self.gps.latDeg if self.gps.latDeg else "0",
                "longitude": self.gps.lonDeg if self.gps.lonDeg else "0",
                "altitude": self.gps.altitude if self.gps.altitude else "0",
                'date': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            }

        else:
            print("reading something")
            location = {
                "latitude": 0,
                "longitude": 0,
                "altitude": 0,
                'date': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            }

        return location


        #################################################################################
    # Database and local Storage                                                    #
    #################################################################################
    def init_db(self):
        if not os.path.exists(self.db_filename):
            with sqlite3.connect(self.db_filename) as conn:
                print('Creating schema')
                with open(self.schema_filename, 'rt') as f:
                    schema = f.read()
                conn.executescript(schema)
                print('Schema created\n\n')
        else:
            print("Database already exists")

    def persist_data(self, data, is_delivered=False):
        if os.path.exists(self.db_filename):
            print("Persisting data")
            with sqlite3.connect(self.db_filename) as conn:
                print("persist reading")
                conn.execute(
                    """
                    INSERT INTO gps (latitude, longitude,altitude, reading_date,is_delivered)
                    VALUES (?,?,?,?,?) 
                    """, (data['location']['latitude'], data['location']['longitude'], data['location']['altitude'],
                          datetime.strptime(data['location']['date'], '%Y-%m-%dT%H:%M:%SZ'), is_delivered)
                )
                for sensor, readings in data['readings'].items():
                    for reading in readings:
                        conn.execute(
                            """
                            INSERT INTO readings (sensor, value, reading_date, is_delivered)
                            VALUES (?,?,?,?) 
                            """, (sensor,
                                  reading['value'],
                                  datetime.strptime(reading['date'], '%Y-%m-%dT%H:%M:%SZ'),
                                  is_delivered)
                        )
                        print("YEY reading")
                conn.commit()
            print("Done: Data persisted")
            return True
        else:
            print("Database still not created. Run init_db() before being able to persiste data")
            return False

    def send_undelivered_data(self):
        if os.path.exists(self.db_filename):
            with sqlite3.connect(self.db_filename) as conn:
                c = conn.cursor()
                c.execute(" SELECT sensor, value, reading_date FROM readings  WHERE is_delivered=0")
                result = c.fetchall()

            if not result:
                return True

            data = {
                "station_id": self.id,
                "location": {  # TODO be able to send data without location
                    "latitude": 42,
                    "longitude": 42,
                    "altitude": 42
                },
                "readings": {row[0]: {'value': row[1], 'date': row[2]} for row in result },
            }
            print("trying to deliver data")
            return True if self.deliver_data(data) else False

