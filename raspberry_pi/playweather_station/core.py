from threading import Thread
import time
from datetime import datetime
from pprint import pprint

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
    def __init__(self):
        self.registered_sensors = {}
        self.data_collector = {}
        self.threads = {}
        self.running = False

    def register(self, sensor_class, name):
        self.registered_sensors[name] = sensor_class(name, self.data_collector)

    def initialize(self):
        print("Initializing sensors... ")

        self.running = True
        self.threads = {}
        for sensor_name, sensor in self.registered_sensors.iteritems():
            self.threads[sensor_name] = sensor
            self.threads[sensor_name].start()
            print("=> sensor: '" + sensor_name + "' is running.")

        for _ in range(10):
            time.sleep(5)
            for key, value in self.data_collector.iteritems():
                print(key, value)
            for sensor in self.data_collector:
                self.data_collector[sensor] = []
            print("*********\n\n\n")

    def stop(self):
        print("Wating for all systems to shutdown")
        self.running = False
        for thread in self.threads.values():
            thread.stop()
            thread.join()

        print("Shutdown successful")
