from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from django.contrib.auth.models import User
from panamapi.models import Customer, Payment

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'date_of_birth',
            'phone_number'
        ]

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'firstName',
            'lastName',
            'merchant',
            'expDate',
            'obscured_num'
        ]


class AccountSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True)
    customer = CustomerSerializer(many=False)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'payments',
            'customer'
        ]

class Account(ViewSet):

    permission_classes = (IsAuthenticated,)

    def list(self, request):

        try:
            customer = Customer.objects.get(user=request.auth.user)
            current_user = User.objects.get(pk=customer.id)

            serialized_user = AccountSerializer(current_user, many=False, context={"request": request})

            return Response(serialized_user.data, status=status.HTTP_200_OK)
        
        except Exception as ex:
            return HttpResponseServerError(ex)