#!/usr/bin/python2
import RPi.GPIO as GPIO
import time
import requests

from playweather_station.core import SensorModule


class Rain(SensorModule):
    def run(self):
        # Cada ve que se vacia, equivale a 0.2794 mm de lluvia
        CALIBRATION = 0.2794

        # Pin del GPIO donde se conecta el sensor
        PIN = 17

        # Setup de los pines de E/S
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Variable para contar la lluvia
        rain = 0

        # Variable para el tiempo
        localTime = 0

        # Funcion de interrupcion para detectar cada vez que se cierra el switch
        def cb(channel):
            global rain
            rain = rain + CALIBRATION

        # Registrar las interrupciones del PIN
        GPIO.add_event_detect(PIN, GPIO.RISING, callback=cb, bouncetime=100)

        # Mostrar los resultados del log
        while self.running:

            localtime = time.localtime()
            timeString = time.strftime("%Y %m %d %H:%M:%S", localtime)
            linea = timeString + " se han registrado %f milimetros de lluvia" % (rain)
            self.collect(rain)
            # requests.get('http://192.168.0.6:8000/api/sensor_reading/new?sensor_name=pluviometro&data={}'.format(linea))
            time.sleep(4)  # Tiempo entre lecturas

        # Cerrar el archivo y limpiar el GPIO
        GPIO.cleanup()
