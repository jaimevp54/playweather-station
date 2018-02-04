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

from rest_framework import viewsets
from api.serializers import SensorSerializer, StationSerializer, SensorReadingSerializer

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
        try:
            if Station.objects.filter(id=data["station_id"]).exists():
                station = Station.objects.get(id=data["station_id"])
                station.location_altitude = float(data["location"]["altitude"])
                station.location_longitude = float(data["location"]["longitude"])
                station.location_latitude = float(data["location"]["latitude"])

                station.last_activity_date = datetime.now()
                station.save()
            else:
                return HttpResponse(f"Station {data['station_id']} is not registered on Playweather Web.\n  ignored.")

            received = []
            ignored = []
            for sensor_id, readings in data['readings'].items():
                if Sensor.objects.filter(
                        id=sensor_id).exists():  # TODO check if this sensor belongs to the right station
                    sensor = Sensor.objects.get(id=sensor_id)
                    for reading in readings:
                        SensorReading.objects.create(
                            sensor=Sensor.objects.get(id=sensor_id),
                            data=float(reading['value']),
                            date=datetime.strptime(reading['date'], '%Y-%m-%dT%H:%M:%SZ')
                        )

                    received.append(sensor_id)
                    sensor.last_activity_date = datetime.now()
                    sensor.save()
                else:
                    ignored.append(sensor_id)
        except KeyError as e:
            return HttpResponse("Format error in input data.")

        response = "\n\n**************************************************************************\n"
        response += "The following sensors are not registered, therefore have been ignorored: \n"
        for sensor_id in ignored:
            response += f" - {sensor_id}\n"
        response += "Please register ignored sensors on Playweather Web Admin site (http://playweather.tk/admin) \n\n"

        response += "Data received succesfully for sensors:\n"
        for sensor_id in received:
            response += f" - {sensor_id}\n"
        return HttpResponse(response)


class ReadReading(View):
    def get(self, request):
        readings = SensorReading.objects.filter(
            sensor_id=request.GET['sensor']
        ).order_by('-date')[:int(request.GET['amount'])]

        response = []
        for reading in list(readings.values('id', 'sensor', 'data', 'date')):
            reading['sensor_id'] = Sensor.objects.get(pk=reading['sensor']).id
            response.append(reading)

        return JsonResponse(response, safe=False)


# SERIALIZER VIEWS HERE


class SensorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class StationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
