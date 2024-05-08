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
            'first_name',
            'last_name',
            'merchant',
            'expiration_date',
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
        """get users account info

        Args:
            request (GET): gets both user and customer instances for a user 

        Returns:
            serialized user info as object with nested "customer" field
        """

        try:
            customer = Customer.objects.get(user=request.auth.user)
            current_user = User.objects.get(pk=customer.id)

            serialized_user = AccountSerializer(current_user, many=False, context={"request": request})

            return Response(serialized_user.data, status=status.HTTP_200_OK)
        
        except Exception as ex:
            return HttpResponseServerError(ex)
        

    def update(self, request, pk=None):
        """edit Users account info

        Args:
            request (PUT): include changes in request data
        """

        customer = Customer.objects.get(user=request.auth.user)
        current_user = User.objects.get(pk=pk)
        customer.date_of_birth = request.data['date_of_birth']
        customer.phone_number = request.data['phone_number']
        current_user.first_name = request.data['first_name']
        current_user.last_name = request.data['last_name']
        current_user.email = request.data['email']
        current_user.save()
        customer.save()

        return Response("account updated", status=status.HTTP_204_NO_CONTENT)
