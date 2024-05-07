"""View module for handling requests about customer payment types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from panamapi.models import Payment, Customer
from django.contrib.auth.models import User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'merchant', 
            'card_number',
            'expiration_date',
            'first_name',
            'last_name',
            'expiration_date' 
            ]



class Payments(ViewSet):

    def create(self, request):
        new_payment = Payment()
        new_payment.first_name = request.data["first_name"]
        new_payment.last_name = request.data["last_name"]
        new_payment.merchant = request.data["merchant"]
        new_payment.card_number = request.data["card_number"]
        new_payment.expiration_date = request.data["expiration_date"]
        new_payment.CVV = request.data["CVV"]
        new_payment.user = request.user
        new_payment.save()

        serialized_payment = PaymentSerializer(
            new_payment, context={'request': request})

        return Response(serialized_payment.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        user = request.user
        payment_type = Payment.objects.get(pk=pk)
        if payment_type.user is user:
            try:
                payment_type = Payment.objects.get(pk=pk)
                serialized_payment = PaymentSerializer(
                    payment_type, context={'request': request})
                return Response(serialized_payment.data)
            except Exception as ex:
                return HttpResponseServerError(ex)
        else:
            return Response("", status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        user = request.user
        payment = Payment.objects.get(pk=pk)
        if payment.user is user:
            try:
                payment.delete()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

            except Payment.DoesNotExist as ex:
                return Response({'payment type deleted': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            except Exception as ex:
                return Response({'payment type does not exist': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response("Not authorized to delete this payment", status=status.HTTP_403_FORBIDDEN)

    def list(self, request):
        user = request.user
        if user.is_authenticated:
            payment_types = Payment.objects.filter(user=user)
        else:
            payment_types = Payment.objects.none()

        serialized_payments = PaymentSerializer(
            payment_types, many=True, context={'request': request})
        
        return Response(serialized_payments.data)
