from playweather_station.core import SensorModule


class CO(SensorModule):
    def setup(self):
        from playweather_station.sensors.helpers.mq import MQ
        self.setup_vars['MQ'] = MQ()

    def capture_data(self):
        mq = self.setup_vars['MQ']
        perc = mq.MQPercentage()
        return perc["CO"]
