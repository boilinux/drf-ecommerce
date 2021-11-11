from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from order import serializers

# Create your views here.


class OrderViews(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', 'get']

    def check_params(self, request):
        if not 'Account' in request.data or not request.data['Account']:
            return Response('User id is required', status=400)
        if not 'total' in request.data or not request.data['total']:
            return Response('Total is required', status=400)
        if not 'datetime' in request.data or not request.data['datetime']:
            return Response('Datetime is required', status=400)
        if not 'phone_number' in request.data or not request.data['phone_number']:
            return Response('Phone number is required', status=400)
        if not 'full_name' in request.data or not request.data['full_name']:
            return Response('Full name is required', status=400)
        if not 'address' in request.data or not request.data['address']:
            return Response('Address is required', status=400)

        return True

    def post(self, request, format=None):
        if self.check_params(request) != True:
            return self.check_params(request)

        try:
            serializer = serializers.OrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response('created', status=201)
        except:
            return Response('something went wrong', status=500)
