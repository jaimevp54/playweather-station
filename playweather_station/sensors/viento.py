#!/usr/bin/python
from playweather_station.core import SensorModule


class Wind(SensorModule):

    def ReadChannel(self,channel):
        adc = self.setup_vars['spi'].xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    # Funcion para convertir el dato a niveles de voltaje
    def ConvertVolts(self,data, places):
        volts = (data * 5.0) / float(1023)
        volts = round(volts, places)
        return volts

    def setup(self):
        import spidev
        import RPi.GPIO as GPIO
        # Cada vez que cierre el contacto equivale a 2.4 Km/h
        self.setup_vars['factor_velocidad'] = 2.4
        self.setup_vars['vane_grados'] = 0
        self.setup_vars['speed'] = 0

        # Pin del GPIO para conectar el sensor de velocidad de viento
        self.setup_vars['PIN'] = 23

        # Setup de los pines E/S
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.setup_vars['PIN'], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Variable para conteo de velocidad

        # Funcion de interrupcion para dectectar cada vez que se cierre el contacto
        def cb(channel):
            self.setup_vars['speed'] = self.setup_vars['speed'] + 2.4

        # Registrar las interrupciones del PIN
        GPIO.add_event_detect(self.setup_vars['PIN'], GPIO.RISING, callback=cb, bouncetime=100)

        # Abrir el bus de SPI
        self.setup_vars['spi']= spidev.SpiDev()
        self.setup_vars['spi'].open(0, 0)

        # Funcion para leer la data del canal por SPI.
        # El canal tiene que ser un entero entre 0 y 7.


        # Definir los canales que usa cada self.setup_vars['sensor
        self.setup_vars['vane_channel']= 1
        self.setup_vars['uv_channel']= 2

        # Definir el delay entre lecturas

        # Variable para el tiempo
        self.setup_vars['localTime']= 0


    def capture_data(self):
        # Leer el dato del sensor de direccion de viento
        vane_level= self.ReadChannel(self.setup_vars['vane_channel'])
        vane_volts= self.ConvertVolts(vane_level, 2)

        if vane_volts >= 3.76 and vane_volts <= 3.79:
            self.setup_vars['vane_grados']= 0
        elif vane_volts >= 1.96 and vane_volts <= 2.00:
            self.setup_vars['vane_grados']= 22.5
        elif vane_volts >= 2.24 and vane_volts <= 2.26:
            self.setup_vars['vane_grados']= 45
        elif vane_volts >= 0.39 and vane_volts <= 0.43:
            self.setup_vars['vane_grados ']= 67.5
        elif vane_volts >= 0.44 and vane_volts <= 0.47:
            self.setup_vars['vane_grados']= 90
        elif vane_volts >= 0.30 and vane_volts <= 0.34:
            self.setup_vars['vane_grados ']= 112.5
        elif vane_volts >= 0.88 and vane_volts <= 0.92:
            self.setup_vars['vane_grados ']= 135
        elif vane_volts >= 0.60 and vane_volts <= 0.64:
            self.setup_vars['vane_grados ']= 157.5
        elif vane_volts >= 1.38 and vane_volts <= 1.42:
            self.setup_vars['vane_grados ']= 180
        elif vane_volts >= 1.18 and vane_volts <= 1.22:
            self.setup_vars['vane_grados ']= 202.5
        elif vane_volts >= 3.03 and vane_volts <= 3.10:
            self.setup_vars['vane_grados ']= 225
        elif vane_volts >= 2.88 and vane_volts <= 2.95:
            self.setup_vars['vane_grados ']= 247.5
        elif vane_volts >= 4.49 and vane_volts <= 4.53:
            self.setup_vars['vane_grados ']= 270
        elif vane_volts >= 3.93 and vane_volts <= 3.98:
            self.setup_vars['vane_grados ']= 292.5
        elif vane_volts >= 4.23 and vane_volts <= 4.28:
            self.setup_vars['vane_grados ']= 315
        elif vane_volts >= 3.37 and vane_volts <= 3.42:
            self.setup_vars['vane_grados ']= 337.5

        result= {
            'direccion': vane_grados,
            'velocidad': self.setup_vars['speed'],
        }
        self.setup_vars['speed'] = 0
        return  result

            

    def cleanup(self):

        # Limpiar el GPIO
        GPIO.cleanup()

        """
        Para 0 grados, un voltaje de 3.76-3.79
        Para 22.5 grados, un voltaje de 1.98
        Para 45 grados, un voltaje de 2.25
        Para 67.5 grados, un voltaje 0.41
        Para 90 grados, un voltaje de 0.45
        Para 112.5 grados, un voltaje de 0.32
        Para 135 grados, un voltaje de 0.90
        Para 157.5 grados, un voltaje 0.62
        Para 180 grados, un voltaje de 1.40
        Para 202.5 grados, un voltaje de 1.19
        Para 225 grados, un voltaje de 3.08
        Para 247.5 grados, un voltaje de 2.93
        Para 270 grados, un voltaje de 4.62
        Para 292.5 grados, un voltaje de 4gg.04
        Para 315 grados, un voltaje de 4.33
        Para 337.5 grados, un voltaje de 3.43
        """

    def _fake_capture_data(self):
        return {
            'velocidad': 42,
            'direccion': 24,
        }
