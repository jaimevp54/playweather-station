
import sys, time

from playweather_station.core import SensorModule 

from playweather_station.core  import *
class CO(SensorModule):
    def run(self, data_collector):
        try:
            print("Presione CTRL+C para abortar.")
            mq = MQ()
            while True:
                perc = mq.MQPercentage()
                print("CO: %g ppm" % (perc["CO"]))
                data_collector['co - ' + str(time.localtime())] = perc["CO"]
                time.sleep(1)

        except:
            print("\nAbortado")
