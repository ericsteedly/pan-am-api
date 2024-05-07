from rest_framework import serializers
from panamapi.models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "booking_id",
            "flight_id",
            "user_id"
        ]
