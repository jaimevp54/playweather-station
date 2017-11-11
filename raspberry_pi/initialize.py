from playweather_station.core import PlayWeatherStation

from playweather_station.sensors import co, DHT22, lluvia, viento

pw = PlayWeatherStation()

# Register module classes in here
# --> pw.register(module.Class)

#pw.register(co.CO,'co')
#pw.register(lluvia.Rain,'lluvia')
pw.register(viento.Wind,'viento')

pw.initialize()
