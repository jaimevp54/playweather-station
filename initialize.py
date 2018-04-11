from playweather_station.core import PlayWeatherStation

from playweather_station.sensors import co, DHT22, lluvia, viento, ccs811, UV

from playweather_station.plugins import weather_underground
from playweather_station.settings import *

import configparser
import logging

logging.basicConfig(filename="/var/log/playweather/core.log", level=logging.DEBUG, format='%(asctime)s [%(levelname)s]  %(message)s',datefmt='%m/%d/%Y %I:%M:%S%p' )


def default_config():
    new_config = configparser.SafeConfigParser()
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
config = configparser.SafeConfigParser()
config.read('config.ini')
# if not validate(config):
#     config = default_config()

config['PLAYWEATHER_STATION']={
    'id': config['PLAYWEATHER_STATION'].get('id','station')  if "PLAYWEATHER_STATION" in config else 'station',
    'delivery_interval': config['PLAYWEATHER_STATION'].get('delivery_interval',30) if "PLAYWEATHER_STATION" in config else 30,
    'delivery_url': DELIVERY_URL,
    'should_deliver_data': SHOULD_DELIVER_DATA,
    'should_persist_data': SHOULD_PERSIST_DATA,
    'should_deliver_weather_underground_data': SHOULD_DELIVER_WEATHER_UNDERGROUND_DATA,
    'gps_on': GPS_ON
}
pw = PlayWeatherStation(fake=FAKE)
pw.delivery_url = DELIVERY_URL
pw.should_deliver_data = SHOULD_DELIVER_DATA
pw.should_persist_data = SHOULD_PERSIST_DATA
pw.should_deliver_weather_underground_data = SHOULD_DELIVER_WEATHER_UNDERGROUND_DATA
pw.gps_on = GPS_ON


# Register module classes in here
# --> pw.register(module.Class)

for sensor in SENSOR_MODULES:
    config[sensor[1]] = {
        'collection_interval': (config[sensor[1]] if config.has_section(sensor[1]) else {}).get('collection_interval',15),
    }
    pw.register(sensor[0],sensor[1])

pw.weather_underground_deliver_data = WEATHER_UNDERGROUND_DELIVERY_METHOD
pw.weather_underground_definitions = WEATHER_UNDERGROUND_DEFINITIONS

with open('config.ini', 'w') as configfile:
    config.write(configfile)

try:
    pw.initialize(config)
except Exception as e:
    logging.exception('An error has occurred: ')
    pw.stop()
finally:
    pw.stop()
