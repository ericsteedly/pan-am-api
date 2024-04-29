from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from panamapi.models import Flight

class Flights(ViewSet):
    def list(self, request):
        
        flights = Flight.objects.all()


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = [
            'id',
            'departureDay',
            'departureTime',
            'arrivalDay',
            'arrivalTime',
            'price',
            'points',
            'seats'
        ]
