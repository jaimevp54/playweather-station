from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from datetime import datetime
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
        data = json.loads(
            '{"pluvial": [{"date": "2017-11-13T20:49:15Z", "value": 0}], "viento_velocidad": [{"date": '
            '"2017-11-13T20:49:16Z", "value": 0}], "co": [{"date": "2017-11-13T20:49:13Z", '
            '"value": 0.004963269307602358}, {"date": "2017-11-13T20:49:16Z", "value": 0.004963269307602358}], '
            '"viento_direccion": [{"date": "2017-11-13T20:49:16Z", "value": 292.5}]}'
        )

        for sensor, readings in data.items():
            for reading in readings:
                SensorReading.objects.create(
                    sensor=Sensor.objects.get(name=sensor),
                    data=float(reading['value']),
                    date=datetime.strptime(reading['date'], '%Y-%m-%dT%H:%M:%SZ')
                )

        return HttpResponse("Data received succesfully ->" + json.dumps(data))

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        for sensor, readings in data.items():
            for reading in readings:
                SensorReading.objects.create(
                    sensor=Sensor.objects.get(name=sensor),
                    data=float(reading['value']),
                    date=datetime.strptime(reading['date'], '%Y-%m-%dT%H:%M:%SZ')
                )

        return HttpResponse("Data received succesfully ->" + json.dumps(data))


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
