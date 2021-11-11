
from rest_framework.fields import empty
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

from store.serializers import StoreSerializer
from store.models import Store, StoreImage
from account.models import Account


class StoreCreateViews(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']

    def post(self, request, format=None):
        data = {}
        try:

            if not 'Account' in request.data or not request.data['Account']:
                return Response('user id is required', status=400)
            if not 'name' in request.data or not request.data['name']:
                return Response('store name is required', status=400)
            if not 'address' in request.data or not request.data['address']:
                return Response('store address is required', status=400)
            if not 'image' in request.data or not request.data['image']:
                return Response('store image is required', status=400)

            store = Store.objects.create(Account=Account.objects.get(
                pk=request.data['Account']), name=request.data['name'], address=request.data['address'], image=request.data['image'])
            serializer = StoreSerializer(store)
            data['status'] = 'created'
            data['store'] = serializer.data
            return Response(data, status=201)
        except:
            return Response('something went wrong', status=404)


class StoreUpdateViews(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']

    def post(self, request, format=None):
        data = {}
        try:
            if not 'store_id' in request.data or not request.data['store_id']:
                return Response('store id is required', status=400)
            if not 'Account' in request.data or not request.data['Account']:
                return Response('user id is required', status=400)
            if not 'name' in request.data or not request.data['name']:
                return Response('store name is required', status=400)
            if not 'address' in request.data or not request.data['address']:
                return Response('store address is required', status=400)
            if not 'image' in request.data or not request.data['image']:
                return Response('store image is required', status=400)

            store = Store.objects.get(
                pk=request.data['store_id'])
            store.name = request.data['name']
            store.address = request.data['address']
            store.image = request.data['image']
            store.save()
            serializer = StoreSerializer(store)
            data['status'] = 'updated'
            data['store'] = serializer.data
            return Response(data, status=200)
        except:
            return Response('something went wrong', status=404)


class StoreDisableViews(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['delete']

    def delete(self, request, pk, format=None):
        data = {}
        try:
            store = Store.objects.get(
                pk=pk)
            store.active = False
            store.save()
            serializer = StoreSerializer(store)
            data['status'] = 'updated'
            data['store'] = serializer.data
            return Response(data, status=200)
        except:
            return Response('something went wrong', status=404)


class StoreImageViews(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', 'delete']

    def post(self, request, format=None):
        try:
            if not 'store_id' in request.data or not request.data['store_id']:
                return Response('store id is required', status=400)
            if not 'image' in request.data or not request.data['image']:
                return Response('image is required', status=400)

            StoreImage.objects.create(Store=Store.objects.get(
                pk=request.data['store_id']), image=request.data['image'])
            return Response('created', status=201)
        except:
            return Response('something went wrong', status=404)

    def delete(self, request, pk, format=None):
        try:
            obj = StoreImage.objects.get(pk=pk)
            obj.delete()
            return Response('deleted', status=200)
        except:
            return Response('something went wrong', status=404)
