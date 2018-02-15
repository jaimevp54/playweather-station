from playweather_station.core import PlayWeatherStation

from playweather_station.sensors import co, DHT22, lluvia, viento, ccs811

from web_server import web_server
import configparser

def default_config():
    new_config = configparser.ConfigParser()
    new_config["PLAYWEATHER_STATION"] = {
        "id": "station",
        "delivery_interval": "5",
    }

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

pw = PlayWeatherStation()

pw.delivery_url = "playweather.fwd.wf"
pw.delivery_port = ""

# Register module classes in here
# --> pw.register(module.Class)

pw.register(co.CO, 'co')
# pw.register(lluvia.Rain, 'pluvial')
# pw.register(DHT22.DHT22, 'DHT22')
# pw.register(viento.Wind, 'viento')
# pw.register(ccs811.CCS811, 'co2')
# pw.register(UV.UV, 'violeta')


# for sensor in pw.registered_sensors:
#     if sensor.upper() not in config:
#         config[sensor.upper()]["id"] = sensor
    
# print("-> writing config file")
# config.write('config.ini')
    
try:
    pw.initialize(config,gps_on=False)
except Exception as e:
    print('An error has occurred: ', e)
    pw.stop()
finally:
    pw.stop()


