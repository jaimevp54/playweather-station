from plugins import weather_underground
from sensors import co, DHT22, lluvia, viento, ccs811, UV

# Station main settings
DELIVERY_URL = "https://playweather-pucmm.herokuapp.com"
DELIVERY_PORT = ""
SHOULD_DELIVER_DATA = True
SHOULD_PERSIST_DATA = False
SHOULD_DELIVER_WEATHER_UNDERGROUND_DATA =True
GPS_ON = True

FAKE = False
# Register module classes in here
# --> pw.register(module.Class)
SENSOR_MODULES = [
    (lluvia.Rain, 'pluvial'),
    (DHT22.DHT22, 'DHT22'),
    (viento.Wind, 'viento'),
    (ccs811.CCS811, 'co2'),
    (UV.UV, 'uv'),
    (co.CO, 'co'),
]

# Define weather underground settings
WEATHER_UNDERGROUND_DELIVERY_METHOD = weather_underground.deliver_data
WEATHER_UNDERGROUND_DEFINITIONS ={
    'winddir': 'viento_direccion',
    'rainin': 'pluvial',
    'windspeedmph': 'viento_velocidad',
    'tempf': 'DHT22_temp',
    'humidity': 'DHT22_humedad',
}
