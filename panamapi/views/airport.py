from rest_framework import serializers, status
from panamapi.models import Airport
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from panamapi.models import Airport

class Airports(ViewSet):
    def list(self, request):
        airports = Airport.objects.all()
        serialized = AirportSerializer(airports, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = [
            'id',
            'name',
            'city',
            'state',
            'country',
            'airport_code'
        ]
