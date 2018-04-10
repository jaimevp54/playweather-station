from playweather_station.core import PlayWeatherStation

from playweather_station.sensors import co, DHT22, lluvia, viento, ccs811, UV

from playweather_station.plugins import weather_underground
from playweather_station.settings import *

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

pw = PlayWeatherStation(fake=FAKE)
pw.delivery_url = DELIVERY_URL
pw.should_deliver_data = SHOULD_DELIVER_DATA
pw.should_persist_data = SHOULD_PERSIST_DATA
pw.should_deliver_weather_underground_data = SHOULD_DELIVER_WEATHER_UNDERGROUND_DATA
pw.gps_on = GPS_ON

# Register module classes in here
# --> pw.register(module.Class)

for sensor in SENSOR_MODULES:
    pw.register(sensor[0],sensor[1])

pw.weather_underground_deliver_data = WEATHER_UNDERGROUND_DELIVERY_METHOD
pw.weather_underground_definitions = WEATHER_UNDERGROUND_DEFINITIONS

try:
    pw.initialize(config)
except Exception as e:
    print('An error has occurred: ', e)
    pw.stop()
finally:
    pw.stop()
