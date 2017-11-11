from threading import Thread
import time
from pprint import pprint

import json


class SensorModule:
    def __init__(self):
        pass

    def run(self, data_collector):
        pass


class PlayWeatherStation:
    def __init__(self):
        self.registered_sensors = {}
        self.data_collector = {}
        self.threads = {}

    def register(self, sensor, name):
        sensor.name = name
        self.registered_sensors[name] = sensor

    def initialize(self):
        print("Initializing sensors... ")
        for sensor in self.registered_sensors:
            self.data_collector[sensor] = []

        print(self.data_collector)

        self.threads = {}

        for sensor in self.registered_sensors:
            self.threads[sensor] = Thread(target=self.registered_sensors[sensor]().run, args=(self.data_collector,))
            self.threads[sensor].start()

        while True:
            time.sleep(5)
            pprint(json.dumps(self.data_collector))
            tmp_collector = {}
            for sensor in self.registered_sensors:
                tmp_collector[sensor] = []
            self.data_collector = dict(tmp_collector)
            print("*********\n\n\n")
