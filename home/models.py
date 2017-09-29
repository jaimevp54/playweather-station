from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Station(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    location_longitude = models.FloatField()
    location_latitude = models.FloatField()
    location_altitude = models.FloatField()

    def __str__(self):
        return f'{self.name} - Owner: {self.owner.username}'


class Sensor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    station = models.ForeignKey(Station)

    def __str__(self):
        return f'{self.name} - Installed at: {self.station.name}'


class SensorReading(models.Model):
    date = models.DateTimeField(auto_now=True)
    data = models.TextField(default="error")
    sensor = models.ForeignKey(Sensor)

    def __str__(self):
        return f'Sensor:{self.sensor.name} at:{self.date}'
