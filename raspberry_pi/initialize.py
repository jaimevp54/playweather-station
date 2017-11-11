from playweather_station.core import PlayWeatherStation

from playweather_station.sensors import co, DHT22, lluvia, viento

pw = PlayWeatherStation()

# Register module classes in here
# --> pw.register(module.Class)

pw.register(co.CO)
pw.register(lluvia.Rain)
pw.register(DHT22.DHY22)
pw.register(viento.Wind)

pw.initialize()
