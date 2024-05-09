from panamapi.models import Ticket, Booking, Flight
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from .booking import BookingSerializer

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "booking_id",
            "flight_id",
            "user_id"
        ]

class Tickets(ViewSet):
    def create(self, request):
        """Create new ticket/tickets objects

        Args:
            request (POST):Object with booking_id key and flights key for List of one or multiple dictionaries containing, 'flight_id'
            ex. [{flight_id: 1}, {flight_id:2 }]
        """


        this_booking = Booking.objects.get(pk=request.data['booking_id'])
        current_user = request.user

        if this_booking.user_id is current_user.id:
        
            flights = request.data['flights']
            for flight in flights:
                flightId = flight["flight_id"]
                ticket = Ticket()
                ticket.flight = Flight.objects.get(pk=flightId)
                ticket.booking = this_booking
                ticket.user = current_user
                ticket.save()

            return Response("New Booking Tickets created", status=status.HTTP_200_OK)
        
    def destroy(self, request, pk=None):
        """
            Delete all tickets on booking being edited
            request (Delete): BOOKING_ID

        """
        current_user = request.user
        this_booking = Booking.objects.get(pk=pk)

        if this_booking.user_id is current_user.id:
            try:
                tickets = Ticket.objects.filter(booking_id=this_booking)
                for ticket in tickets:
                    ticket.delete()

            except Booking.DoesNotExist as ex:
                return Response({"No Tickets found on this Booking": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            return Response("Booking Tickets Deleted", status=status.HTTP_200_OK)
        else:
            return Response("Not authorized to delete tickets", status=status.HTTP_403_FORBIDDEN)