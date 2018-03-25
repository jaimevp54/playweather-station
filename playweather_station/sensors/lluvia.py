#!/usr/bin/python2
import time

from playweather_station.core import SensorModule


class Rain(SensorModule):

    def cb(self,channel):
        self.setup_vars['rain'] += self.setup_vars['calibration']

    def setup(self):
        import RPi.GPIO as GPIO

        self.setup_vars['calibration']= 0.2794
        self.setup_vars['PIN']= 24

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.setup_vars['PIN'], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Variable para contar la lluvia
        self.setup_vars['rain'] = 0

        # Variable para el tiempo
        self.setup_vars['localTime'] = 0

        # Funcion de interrupcion para detectar cada vez que se cierra el switch
        # Registrar las interrupciones del PIN
        GPIO.add_event_detect(self.setup_vars['PIN'], GPIO.RISING, callback=self.cb, bouncetime=100)


    def capture_data(self):

        localtime = time.localtime()
        timeString = time.strftime("%Y %m %d %H:%M:%S", localtime)
        linea = timeString + " se han registrado %f milimetros de lluvia" % (self.setup_vars['rain'])
        return self.setup_vars['rain']

    def cleanup(self):
        GPIO.cleanup()
