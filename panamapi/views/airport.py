from rest_framework import serializers
from panamapi.models import Airport

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