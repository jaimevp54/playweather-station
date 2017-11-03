from mq import *
import sys, time

try:
    print("Presione CTRL+C para abortar.")
    
    mq = MQ();
    while True:
        perc = mq.MQPercentage()
        print("CO: %g ppm" % (perc["CO"]))
        time.sleep(1)

except:
    print("\nAbortado")
