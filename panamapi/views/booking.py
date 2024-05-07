import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from django.contrib.auth.models import User
from panamapi.models import Customer, Booking, Ticket, Flight, RoundTrip
from rest_framework.decorators import action
from .flight import FlightSerializer

class TicketSerializer(serializers.ModelSerializer):
    flight = FlightSerializer(many=False)
    class Meta:
        model = Ticket
        fields = [
            "id",
            "booking_id",
            "flight",
            "user_id"
        ]

class BookingSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "user_id",
            "payment_id",
            "rewards_payment",
            "tickets",
            "total_price"
        ]

class RoundTripSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoundTrip
        fields = [
            "id",
            "departure_booking",
            "return_booking"
        ]


class Bookings(ViewSet):

    def create(self, request):
        """Create a new Booking and create a ticket for a flight

        Args:
            request (POST): List of one or multiple dictionaries containing, 'flight_id'
            ex. [{flight_id: 1}, {flight_id:2 }]
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        new_booking = Booking()
        new_booking.user = current_user
        new_booking.save()
        
        flights = request.data
        for flight in flights:
            flightId = flight["flight_id"]
            ticket = Ticket()
            ticket.flight = Flight.objects.get(pk=flightId)
            ticket.booking = new_booking
            ticket.user = current_user
            ticket.save()

        serialized_booking = BookingSerializer(new_booking, context={"request": request})
        return Response(serialized_booking.data, status=status.HTTP_200_OK)

    def delete(self, request):
        current_user = User.objects.get(pk=request.auth.user.id)

        """
            Delete all tickets in open booking and booking
            request (Delete): Booking_id

        """
        try:
            booking = Booking.objects.get(pk=request.data['booking_id'], user=current_user)
            booking.delete()
        except Booking.DoesNotExist as ex:
            return Response({"This booking does not exist": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def retrieve(self, request, pk=None):
        try:
            current_user = User.objects.get(pk=request.auth.user.id)
            booking = Booking.objects.get(pk=pk, user=current_user)
            serialized_booking = BookingSerializer(booking, context={"request": request})
            return Response(serialized_booking.data)

        except Booking.DoesNotExist as ex:
            return Response(
                {
                "message": "The requested booking does not exist, or you do not have permission to access it."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        """
            List all completed bookings
  
        """
        current_user = Customer.objects.get(user=request.auth.user)
        try:
            completed_bookings = Booking.objects.get(customer=current_user, payment_id__isnull=False)

            # booking_tickets = Ticket.objects.filter(booking=completed_booking)

            serialized_booking = BookingSerializer(
                completed_bookings, many=True, context={"request": request}
            )

        except Booking.DoesNotExist as ex:
            return Response({"No Bookings": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        return Response(serialized_booking.data, status=status.HTTP_200_OK)
    
    @action(methods=["post"], detail=False)
    def roundtrip(self, request):

        if request.method == "POST":
            roundtrip = RoundTrip()
            roundtrip.departure_booking = Booking.objects.get(pk=request.data['departure_id'])
            roundtrip.return_booking = Booking.objects.get(pk=request.data['return_id'])
            roundtrip.save()
            
            serialized_roundtrip = RoundTripSerializer(roundtrip, many=False, context={"request":request})

            return Response(serialized_roundtrip.data, status=status.HTTP_200_OK)
        
    
