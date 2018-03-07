import sys, time

##from playweather_station.core import SensorModule

from playweather_station.sensors.helpers.mq import MQ


class CO(SensorModule):
    def setup(self):
        self.setup_vars['MQ'] = MQ()

    def capture_single_data(self):
        mq = self.setup_vars['MQ']
        perc = mq.MQPercentage()
        print("CO: %g ppm" % (perc["CO"]))
        return perc["CO"]

