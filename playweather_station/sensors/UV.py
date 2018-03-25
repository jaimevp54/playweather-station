from playweather_station.core import SensorModule



class UV(SensorModule):
    # UV_channel = 2

    def setup(self):
        import spidev
        self.setup_vars['spi'] = spidev.SpiDev()
        self.setup_vars['spi'].open(0, 0)

    def capture_data(self):
        uv_level = ReadChannel(2)
        uv_volts = ConvertVolts(uv_level, 2)
        self.collect(uv_volts / 0 / 1)

    def ReadChannel(channel):
        adc = spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def ConvertVolts(data, places):
        volts = (data * 5.0) / (float(1023))
        volts = round(volts, places)
        return volts

