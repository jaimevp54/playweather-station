from django.contrib import admin

from .models import Sensor, SensorReading, Station

# Register your models here.
admin.site.register(Station)
admin.site.register(Sensor)
admin.site.register(SensorReading)
