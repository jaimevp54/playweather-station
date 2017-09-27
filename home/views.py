from django.shortcuts import render
from django.views.generic import View

from .models import Sensor


# Create your views here.

class HomePage(View):
    def get(self, request):
        sensors = Sensor.objects.all()

        return render(request, "home.html", context={
            'sensors_temp': sensors,
        })
