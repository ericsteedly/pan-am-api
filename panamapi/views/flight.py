from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from panamapi.models import Flight, Airport
from .airport import AirportSerializer
from datetime import date, datetime, timedelta
import json


class Flights(ViewSet):
    def list(self, request):
        departureAirport_id = self.request.query_params.get('departureAirport', None)
        arrivalAirport_id = self.request.query_params.get('arrivalAirport', None)
        departure_day = self.request.query_params.get('departureDay', None)

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
        all_flights = list(FlightSerializer(direct_flights, many=True).data) + one_stop_flights

        def get_departure_time(flight):
            if 'flight1' in flight:
                return flight['flight1']['departureTime']
            else:
                return flight['departureTime']

        all_flights.sort(key=get_departure_time)
        ordered_flights = all_flights

        return Response(ordered_flights, status=status.HTTP_200_OK)

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
                    departure_datetime = datetime.combine(flight2.departureDay, flight2.departureTime)
                    layover = departure_datetime - arrival_datetime
                    total_duration = str(flight1.duration + flight2.duration + layover)
                    total_price = flight1.price + flight2.price
                    total_points = flight1.points + flight2.points
                    one_stop_flight = OneStopSerializer({
                        'flight1': flight1,
                        'flight2': flight2,
                        'total_duration': total_duration,
                        'total_price': total_price,
                        'total_points': total_points
                    }).data
                    one_stop_flights.append(one_stop_flight)

        return one_stop_flights

    
class FlightSerializer(serializers.ModelSerializer):
    departureAirport = AirportSerializer(many=False)
    arrivalAirport = AirportSerializer(many=False)
    duration = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

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
            'arrivalAirport',
            'duration'
        ]

    def get_duration(self, obj):
        duration = str(obj.duration)
        return duration
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price'] = float(data['price'])  
        return data

    
class DurationField(serializers.Field):
    def to_representation(self, value):
        seconds = value
        formatted_duration = str(seconds)
        return formatted_duration

class OneStopSerializer(serializers.Serializer):
    flight1 = FlightSerializer(many=False)
    flight2 = FlightSerializer(many=False)
    total_duration = DurationField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_points = serializers.IntegerField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total_price'] = float(data['total_price'])  
        return data
    
