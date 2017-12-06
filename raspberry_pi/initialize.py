from playweather_station.core import PlayWeatherStation

from playweather_station.sensors import co, DHT22, lluvia, viento, ccs811

pw = PlayWeatherStation()

# Register module classes in here
# --> pw.register(module.Class)

pw.register(co.CO, 'co')
pw.register(lluvia.Rain, 'pluvial')
pw.register(DHT22.DHT22, 'DHT22')
pw.register(viento.Wind, 'viento')
pw.register(ccs811.CCS811, 'co2')

try:
    pw.initialize()
except Exception as e:
    print('An error has occurred: ', e)
    pw.stop()
finally:
    pw.stop()