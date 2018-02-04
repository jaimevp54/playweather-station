from rest_framework import serializers
from django.contrib.auth.models import User

from home.models import Station, Sensor, SensorReading


class SensorReadingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SensorReading
        fields = ('data', 'date')


class SensorSerializer(serializers.HyperlinkedModelSerializer):
    readings = SensorReadingSerializer(many=True,)

    class Meta:
        model = Sensor
        fields = ('id', 'description', 'type', 'station', 'readings')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class StationSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.StringRelatedField()
    sensors = serializers.HyperlinkedRelatedField(many=True,read_only=True, view_name='sensor-detail')
    class Meta:
        model = Station
        fields = ('id','name', 'owner', 'sensors')


