from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from account.models import Account
from cart import serializers
from cart.models import LineItem
from product.models import Product

# Create your views here.


class CartViews(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', 'delete']

    def check_params(self, request):
        if not 'Account' in request.data or not request.data['Account']:
            return Response('User id is required', status=400)
        if not 'Product' in request.data or not request.data['Product']:
            return Response('Product id is required', status=400)
        if 'Order' in request.data:
            return Response('Order is not required', status=400)
        if not 'title' in request.data or not request.data['title']:
            return Response('Title is required', status=400)
        if not 'description' in request.data or not request.data['description']:
            return Response('Description is required', status=400)
        if 'price' in request.data:
            return Response('Price is not required because its auto update', status=400)
        if not 'quantity' in request.data or not request.data['quantity']:
            return Response('Quantity is required', status=400)

        return True

    def post(self, request, format=None):
        if self.check_params(request) != True:
            return self.check_params(request)

        try:
            item = LineItem.objects.get(
                Account_id=request.data['Account'], Product_id=request.data['Product'], Order=None)
            serializer = serializers.CartSerializer(
                LineItem, data=request.data)
            if serializer.is_valid():
                product = Product.objects.get(pk=request.data['Product'])
                item.quantity = int(item.quantity) + \
                    int(request.data['quantity'])
                item.price = "{:.2f}".format(
                    float(product.price) * int(item.quantity))
                item.save()
                return Response('cart item updated', status=200)
            return Response('something went wrong', status=500)
        except LineItem.DoesNotExist:
            try:
                product = Product.objects.get(pk=request.data['Product'])

                LineItem.objects.create(
                    Account=Account.objects.get(pk=request.data['Account']),
                    Product=Product.objects.get(pk=request.data['Product']),
                    Order=None,
                    title=request.data['title'],
                    description=request.data['description'],
                    price="{:.2f}".format(float(product.price)),
                    quantity=request.data['quantity']
                )

                return Response('created', status=201)
            except:
                return Response('something went wrong', status=500)

    def delete(self, request, pk, format=None):
        try:
            item = LineItem.objects.get(pk=pk)
            item.delete()
            return Response('cart item deleted', status=200)
        except LineItem.DoesNotExist:
            return Response('cart item not found', status=404)
