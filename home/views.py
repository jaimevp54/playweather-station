from django.shortcuts import render
from django.views.generic import View

from .models import Station, Sensor


# Create your views here.

class DashboardPage(View):
    def get(self, request):
        return render(request, "index.html", context={
            'stations': Station.objects.all(),
            'recent_stations': Station.objects.order_by('date_registered').reverse()[:5],
            'sensors': Sensor.objects.all(),
            'active_stations_count': Station.objects.filter(is_active=True).count(),
            'active_sensors_count': Sensor.objects.filter(is_active=True).count()
        })


class StationIndexPage(View):
    def get(self,request, *args, **kwargs):
        return render(request, "station/index.html", context={
            'stations': Station.objects.all()
        })

class StationViewPage(View):
    def get(self,request, *args, **kwargs):
        station = kwargs["station_id"]
        return render(request, "station/view.html", context={
            'station': Station.objects.get(id=station)
        })
