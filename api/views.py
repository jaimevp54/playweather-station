from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.core.paginator import Paginator
from django.core import serializers

from home.models import Station, Sensor, SensorReading
from django.http import HttpResponse, JsonResponse

import json


# Create your views here.

class NewReading(View):
    def get(self, request):
        reading = SensorReading.objects.create(
            sensor=Sensor.objects.get(name=request.GET['sensor_name']),
            data=request.GET['data'],
        )

        return HttpResponse("Data received succesfully" + reading.data)


@method_decorator(csrf_exempt, name='dispatch')
class NewReadingsBundle(View):
    def get(self, request):
        data = json.loads('{"CO2":234,"dir_viento":192}')
        for sensor in data:
            SensorReading.objects.create(
                sensor=Sensor.objects.get(name=sensor),
                data=data[sensor]
            )
        return HttpResponse("Data received succesfully ->" + json.dumps(data))

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        for sensor in data:
            SensorReading.objects.create(
                sensor=Sensor.objects.get(name=sensor),
                data=data[sensor]
            )

        return HttpResponse("Data received succesfully" + json.dumps(data))


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
