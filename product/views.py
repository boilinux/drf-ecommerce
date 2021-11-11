from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from account.models import Account
from product.models import Favorites, Product, ProductImage
from store.models import Store

# Create your views here.


class ProductViews(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', 'put', 'delete']

    def check_params(self, request, action='post'):
        if not 'Store' in request.data or not request.data['Store']:
            return Response('Store id is required', status=400)
        if not 'title' in request.data or not request.data['title']:
            return Response('Product title is required', status=400)
        if not 'description' in request.data or not request.data['description']:
            return Response('Product description is required', status=400)
        if not 'price' in request.data or not request.data['price']:
            return Response('Product price is required', status=400)
        if not 'image' in request.data or not request.data['image']:
            return Response('Product image is required', status=400)
        if action == 'put':
            if not 'product_id' in request.data or not request.data['product_id']:
                return Response('Product is is required', status=400)

        return True

    def post(self, request, pk=None, format=None):
        if self.check_params(request) != True:
            return self.check_params(request)

        try:
            Product.objects.create(
                Store=Store.objects.get(pk=request.data['Store']), title=request.data['title'], description=request.data[
                    'description'], price=request.data['price'], image=request.data['image']
            )
            return Response('created', status=201)
        except:
            return Response('something went wrong', status=500)

    def put(self, request, pk=None, format=None):
        if self.check_params(request, 'put') != True:
            return self.check_params(request, 'put')

        try:
            product = Product.objects.get(pk=request.data['product_id'])
            product.title = request.data['title']
            product.description = request.data['description']
            product.price = request.data['price']
            product.image = request.data['image']

            product.save()
            return Response('success', status=200)
        except:
            return Response('something went wrong', status=500)

    def delete(self, request, pk=None, format=None):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response('deleted', status=200)
        except:
            return Response('product not found', status=404)


class ProductFavoriteViews(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']

    def check_params(self, request):
        if not 'product_id' in request.data or not request.data['product_id']:
            return Response('Product id is required', status=400)
        if not 'user_id' in request.data or not request.data['user_id']:
            return Response('User id is required', status=400)
        if not 'isfavorite' in request.data or not request.data['isfavorite']:
            return Response('isfavorite is required', status=400)

        return True

    def post(self, request, format=None):
        if self.check_params(request) != True:
            return self.check_params(request)

        try:
            fav = Favorites.objects.get(
                Account=request.data['user_id'], Product=request.data['product_id'])
            fav.isfavorite = request.data['isfavorite']
            fav.save()

        except Favorites.DoesNotExist:
            Favorites.objects.create(
                Account=Account.objects.get(pk=request.data['user_id']),
                Product=Product.objects.get(pk=request.data['product_id']),
                isfavorite=request.data['isfavorite']
            )

        return Response('ok', status=200)


class ProductImagesViews(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', 'delete']

    def check_params(self, request):
        if not 'image' in request.data or not request.data['image']:
            return Response('Image is required', status=400)

        return True

    def post(self, request, product_id, format=None):
        if self.check_params(request) != True:
            return self.check_params(request)

        try:
            product = Product.objects.get(pk=product_id)
            ProductImage.objects.create(
                Product=product, image=request.data['image'])
            return Response('created', status=201)
        except Product.DoesNotExist:
            return Response('product does not exist', status=404)

    def delete(self, request, product_id, image_id, format=None):
        try:
            Product.objects.get(pk=product_id)
            try:
                ProductImage.objects.get(
                    Product=product_id, image=image_id)
                return Response('deleted', status=200)
            except ProductImage.DoesNotExist:
                return Response('image does not exist', status=404)
        except Product.DoesNotExist:
            return Response('product does not exist', status=404)
