from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator
from django.core import serializers

from home.models import Station, Sensor, SensorReading
from django.http import HttpResponse, JsonResponse


# Create your views here.

class NewReading(View):
    def get(self, request):
        reading = SensorReading.objects.create(
            sensor=Sensor.objects.get(name=request.GET['sensor_name']),
            data=request.GET['data'],
        )

        return HttpResponse("Data received succesfully" + reading.data)


class ReadReading(View):
    def get(self, request):
        readings = SensorReading.objects.filter(
            sensor_id=request.GET['sensor']
        ).order_by('-date')[:int(request.GET['amount'])]

        response = []
        for reading in list(readings.values('id', 'sensor', 'data', 'date')):
            reading['sensor_name'] = Sensor.objects.get(pk=reading['sensor']).name
            response.append(reading)
        return JsonResponse(response, safe=False)
