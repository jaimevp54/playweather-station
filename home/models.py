from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class Station(models.Model):
    TIME_TO_WAIT = 60  # Time to wait for activity before declaring station as inactive IN SECONDS

    owner = models.ForeignKey(User)
    id = models.CharField(primary_key=True, max_length=255)  # TODO must be unique
    name = models.CharField(max_length=255, unique=True)  # TODO must be unique
    # city = models.ForeignKey("cities_light.City", null=True, on_delete=models.SET_NULL)
    location_longitude = models.FloatField(null=True, editable=False)
    location_latitude = models.FloatField(null=True, editable=False)
    location_altitude = models.FloatField(null=True, editable=False)
    last_activity_date = models.DateTimeField(null=True, default=datetime.min)
    date_registered = models.DateTimeField(auto_now=True)

    @property
    def sensor_count(self):
        return len(self.sensor_set)

    def __str__(self):
        return f'{self.name} - Owner: {self.owner.username}'


class Sensor(models.Model):
    TIME_TO_WAIT = 60  # Time to wait for activity before declaring sensor as inactive IN SECONDS
    TYPE_CHOICES = [
        ('P', 'Pluvial'),
        ('WS', 'Velocidad Viento'),
        ('WD', 'Direccion Viento'),
        ('UV', 'Ultra Violeta'),
        ('TEMP', 'Temperatura'),
        ('HUM', 'Humedad'),
        ('CO', 'CO'),
        ('CO2', 'CO2')
    ]
    id = models.CharField(primary_key=True, max_length=255)
    description = models.TextField(blank=True)  # TODO can be null
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, default='Pluvial')

    station = models.ForeignKey(Station)
    date_registered = models.DateTimeField(auto_now=True)
    last_activity_date = models.DateTimeField(null=True, default=datetime.min)

    @property
    def measure_unit(self):
        return {
            'P': 'Pluvial',
            'WS': 'Velocidad Viento',
            'WD': 'Direccion Viento',
            'UV': 'UV',
            'TEMP': 'Temperatura',
            'HUM': 'Humedad',
            'CO': 'CO',
            'CO2': 'CO2'
        }[self.type]

    def __str__(self):
        return f'{self.id} - Installed at: {self.station.name}'


class SensorReading(models.Model):
    date = models.DateTimeField(auto_now=True)
    data = models.TextField(default="error")
    sensor = models.ForeignKey(Sensor)

    def __str__(self):
        return f'Sensor:{self.sensor.id} at:{self.date}'
