from threading import Thread
import time


class SensorModule:
    def __init__(self):
        pass

    def run(self, data_collector):
        pass


class PlayWeatherStation:
    def __init__(self):
        self.registered_sensors = []

    def register(self, sensor):
        self.registered_sensors.append(sensor)

    def initialize(self):
        print("Initializing sensors... ")
        data_collector = {}
        threads = {}
        for sensor in self.registered_sensors:
            threads[sensor.__name__] = Thread(target=sensor.run, args=(data_collector,))
            threads[sensor.__name__].start()

        while True:
            time.sleep(5)
            print("\n\n\n*********")
            print("acumulado")
            for l in data_collector:
                print(l, data_collector[l])
            data_collector.clear()
            print("*********\n\n\n")
            for t in threads:
                threads[t].terminate()
            break
