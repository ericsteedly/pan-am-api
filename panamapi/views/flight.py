from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from panamapi.models import Flight, Airport
from .airport import AirportSerializer
from datetime import date, datetime, timedelta


class Flights(ViewSet):
    def list(self, request):
        departureAirport_id = request.data.get('departureAirport')
        arrivalAirport_id = request.data.get('arrivalAirport')
        departure_day = request.data.get('departureDay')

        try:
            departure_airport = Airport.objects.get(pk=departureAirport_id)
            arrival_airport = Airport.objects.get(pk=arrivalAirport_id)
            departure_day = date.fromisoformat(departure_day)
        except Airport.DoesNotExist:
            return Response({'error': 'Invalid airport id.'}, status=400)
        except ValueError:
            return Response({'error': 'Invalid date format.'}, status=400)

        direct_flights = Flight.objects.filter(
            departureAirport=departure_airport,
            arrivalAirport=arrival_airport,
            departureDay=departure_day
        )

        one_stop_flights = self.get_one_stop_flights(departure_airport, arrival_airport, departure_day)

        all_flights = list(FlightSerializer(direct_flights, many=True).data) + list(one_stop_flights)

        return Response(all_flights, status=status.HTTP_200_OK)

    def get_one_stop_flights(self, departure_airport, arrival_airport, departure_day):
        one_stop_flights = []
        airports = Airport.objects.exclude(pk__in=[departure_airport.pk, arrival_airport.pk])

        for airport in airports:
            first_leg = Flight.objects.filter(
                departureAirport=departure_airport,
                arrivalAirport=airport,
                departureDay=departure_day
            )

            for flight1 in first_leg:
                arrival_datetime = datetime.combine(flight1.arrivalDay, flight1.arrivalTime)
                min_departure_datetime = arrival_datetime + timedelta(minutes=30) #create parameter for minimum layover of 30 minutes
                max_departure_datetime = arrival_datetime + timedelta(hours=3) #create parameter for max layover of 3 hours

                second_leg = Flight.objects.filter(
                    departureAirport=airport,
                    arrivalAirport=arrival_airport,
                    departureDay__gte=min_departure_datetime.date(),
                    departureTime__gte=min_departure_datetime.time(),
                    departureTime__lte=max_departure_datetime.time()
                )

                for flight2 in second_leg:
                    serialized_flight1 = FlightSerializer(flight1, many=False).data
                    serialized_flight2 = FlightSerializer(flight2, many=False).data
                    one_stop_flight = [serialized_flight1, serialized_flight2]
                    one_stop_flights.append(one_stop_flight)

        return one_stop_flights

    
class FlightSerializer(serializers.ModelSerializer):
    departureAirport = AirportSerializer(many=False)
    arrivalAirport = AirportSerializer(many=False)

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
            'seats',
            'departureAirport',
            'arrivalAirport'
        ]
