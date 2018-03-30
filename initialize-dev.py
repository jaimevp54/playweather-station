from playweather_station.core import PlayWeatherStation

from playweather_station.sensors import co, DHT22, lluvia, viento, ccs811, UV

from playweather_station.plugins import weather_underground

import configparser


def default_config():
    new_config = configparser.ConfigParser()
    new_config["PLAYWEATHER_STATION"] = {
        "id": "station",
        "delivery_interval": "5",
    }
    return new_config


def validate(config):
    if "PLAYWEATHER_STATION" not in config:
        return False
    if "id" not in config["PLAYWEATHER_STATION"]:
        return False
    return True


# read configuration file
config = configparser.ConfigParser()
config.read('config.ini')

if not validate(config):
    config = default_config()

pw = PlayWeatherStation(fake=True)
pw.delivery_url = "https://playweather-pucmm.herokuapp.com"
pw.delivery_port = ""
pw.should_deliver_data = False
pw.should_persist_data = False
pw.gps_on = False

# Register module classes in here
# --> pw.register(module.Class)

pw.register(lluvia.Rain, 'pluvial')
pw.register(DHT22.DHT22, 'DHT22')
pw.register(viento.Wind, 'viento')
pw.register(ccs811.CCS811, 'co2')
pw.register(UV.UV, 'uv')
pw.register(co.CO, 'co')

pw.weather_underground_deliver_data = weather_underground.deliver_data
pw.weather_underground_definitions ={
    'winddir': 'viento_direccion',
    'rainin': 'pluvial',
    'windspeedmph': 'viento_velocidad',
    # 'tempf': 'DHT22_temp',
    # 'humidity': 'DHT22_humedad',
}


try:
    pw.initialize(config)
except Exception as e:
    print('An error has occurred: ', e)
    pw.stop()
finally:
    pw.stop()

