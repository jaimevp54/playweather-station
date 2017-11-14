from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Station(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    city = models.ForeignKey("cities_light.City", null=True, on_delete=models.SET_NULL)
    location_longitude = models.FloatField()
    location_latitude = models.FloatField()
    location_altitude = models.FloatField()
    is_active = models.BooleanField()
    date_registered = models.DateTimeField(auto_now=True)

    @property
    def sensor_count(self):
        return len(self.sensor_set)

    def __str__(self):
        return f'{self.name} - Owner: {self.owner.username}'


class Sensor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=255, choices=[
        ('P', 'Pluvial'),
        ('WS', 'Velocidad Viento'),
        ('WD', 'Direccion Viento'),
        ('UV', 'Luz Ultra Violeta)'),
        ('CO', 'CO'),
        ('CO2', "CO2")
    ], default='Pluvial')
    station = models.ForeignKey(Station)
    is_active = models.BooleanField()
    date_registered = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - Installed at: {self.station.name}'


class SensorReading(models.Model):
    date = models.DateTimeField(auto_now=True)
    data = models.TextField(default="error")
    sensor = models.ForeignKey(Sensor)

    def __str__(self):
        return f'Sensor:{self.sensor.name} at:{self.date}'
