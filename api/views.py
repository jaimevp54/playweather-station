from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from datetime import datetime
from django.core.paginator import Paginator
from django.core import serializers

from home.models import Station, Sensor, SensorReading
from django.http import HttpResponse, JsonResponse

from pprint import pprint
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
        pprint(data)

        if Station.objects.filter(station_id=data["station_id"]).exists():
            station = Station.objects.get(_id=data["station_id"])
            station.location_altitude = data["location"]["altitude"]
            station.location_longitude = data["location"]["longitude"]
            station.location_latitude = data["location"]["latitude"]
        else:
            return HttpResponse(f"Station {data['station_id']} is not registered on Playweather Web.\n  ignored.")

        received = []
        ignored = []
        for sensor, readings in data['readings'].items():
            if Sensor.objects.filter(sensor_id=sensor).exists():  # TODO check if this sensor belongs to the right station
                received.append(sensor)
                for reading in readings:
                    SensorReading.objects.create(
                        sensor=Sensor.objects.get(sensor_id=sensor),
                        data=float(reading['value']),
                        date=datetime.strptime(reading['date'], '%Y-%m-%dT%H:%M:%SZ')
                    )
            else:
                ignored.append(sensor)

        response = ""
        response += "The following sensors are not registered, therefore have been ignorored: \n"
        for sensor in ignored:
            response += f" - {sensor}\n"
        response += "Please register ignored sensors on Playweather Web Admin site (http://playweather.tk/admin) \n\n"

        response += "Data received succesfully for sensors:\n"
        for sensor in received:
            response += f" - {sensor}\n"
        return HttpResponse(response)


class ReadReading(View):
    def get(self, request):
        readings = SensorReading.objects.filter(
            sensor_id=request.GET['sensor']
        ).order_by('-date')[:int(request.GET['amount'])]

        response = []
        for reading in list(readings.values('id', 'sensor', 'data', 'date')):
            reading['sensor_id'] = Sensor.objects.get(pk=reading['sensor']).name
            response.append(reading)
        return JsonResponse(response, safe=False)
