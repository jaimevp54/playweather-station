import mq, sys, time



def capture_single_data(self):
    mq = self.setup_vars['MQ']
    perc = mq.MQPercentage()
    print("CO: %g ppm" % (perc["CO"]))
    return perc["CO"]

while True:
    capture_single_data()
