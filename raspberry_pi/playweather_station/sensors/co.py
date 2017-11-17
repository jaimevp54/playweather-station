import sys, time

from playweather_station.core import SensorModule

from playweather_station.sensors.helpers.mq import MQ


class CO(SensorModule):
    def run(self):
        try:
            mq = MQ()

            while self.running:
                perc = mq.MQPercentage()
                print("CO: %g ppm" % (perc["CO"]))
                self.collect(perc["CO"])
                time.sleep(3)
        except Exception as e:
            print("\nAbortado: ", e.message)
