from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Station(models.Model):
    owner = models.ForeignKey(User)
    id = models.CharField(primary_key=True, max_length=255)  # TODO must be unique
    name = models.CharField(max_length=255, unique=True)  # TODO must be unique
    # city = models.ForeignKey("cities_light.City", null=True, on_delete=models.SET_NULL)
    location_longitude = models.FloatField(null=True, editable=False)  # TODO can be null
    location_latitude = models.FloatField(null=True, editable=False)  # TODO can be null
    location_altitude = models.FloatField(null=True, editable=False)  # TODO can be null
    is_active = models.BooleanField(editable=False, default=False)
    date_registered = models.DateTimeField(auto_now=True)

    @property
    def sensor_count(self):
        return len(self.sensor_set)

    def __str__(self):
        return f'{self.name} - Owner: {self.owner.username}'


class Sensor(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    description = models.TextField(blank=True)  # TODO can be null
    type = models.CharField(max_length=255, choices=[
        ('P', 'Pluvial'),
        ('WS', 'Velocidad Viento'),
        ('WD', 'Dirsensor_ideccion Viento'),
        ('UV', 'UV'),
        ('TEMP', 'Temperatura'),
        ('HUM', 'Humedad'),
        ('CO', 'CO'),
        ('CO2', 'CO2')

    ], default='Pluvial')
    station = models.ForeignKey(Station)
    is_active = models.BooleanField(editable=False, default=False)
    date_registered = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - Installed at: {self.station.name}'


class SensorReading(models.Model):
    date = models.DateTimeField(auto_now=True)
    data = models.TextField(default="error")
    sensor = models.ForeignKey(Sensor)

    def __str__(self):
        return f'Sensor:{self.sensor.id} at:{self.date}'
