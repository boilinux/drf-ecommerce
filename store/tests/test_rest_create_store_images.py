from rest_framework.test import APIRequestFactory, force_authenticate
from django.urls import resolve
from django.test import TestCase
from account import views as AccountViews
from account import models as AccountModels
from store import models as StoreModels
from store import views as StoreViews
from store import serializers


class CreateStoreImages(TestCase):
    def setUp(self):
        self.client = APIRequestFactory()
        self.response = self.client.post('/api/v1/account/register',
                                         {'username': '09499272717', 'password': 'password1', 'password2': 'password1', 'email': '09499272761@localhost.local', 'full_name': 'stephen wenceslao'})
        self.response = AccountViews.AccountRegisterViews.as_view()(self.response)
        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data['status'], 'created')

        self.response = self.client.post('/api/v1/account/login',
                                         {'username': '09499272717', 'password': 'password1'})
        self.response = AccountViews.AccountLoginViews.as_view()(self.response)
        self.userToken = self.response.data['token']

        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.data['status'], 'login')

        self.user1Obj = AccountModels.Account.objects.get(
            pk=self.response.data['user_info']['id'])
        self.assertEqual(self.user1Obj.username, '09499272717')

        self.response = self.client.post('/api/v1/store/create',
                                         {'name': 'my store', 'Account': self.user1Obj.id, 'address': 'cebu city', 'image': '/files/mystore_image.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreCreateViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data['status'], 'created')

        self.mystore = self.response.data['store']

        self.response = self.client.post(
            '/api/v1/store/image', data={
                'store_id': self.mystore['id'], 'image': '/files/testpic.jpg'
            })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreImageViews.as_view()(
            self.response)

        self.resObj = self.response.data

        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data,
                         'created')

    def test_url_name_store(self):
        resolver = resolve(
            '/api/v1/store/image')
        self.assertEqual(resolver.view_name, 'store:create_image')

    def test_store_images_serializer(self):
        self.serializer = serializers.StoreImageSerializer(
            StoreModels.StoreImage.objects.get(Store=self.mystore['id']))

        self.assertEqual(self.serializer.data, {
                         'id': self.serializer.data['id'], 'image': '/files/testpic.jpg', 'Store': self.mystore['id']})

    def test_created_image_from_store(self):
        self.assertEqual(self.resObj, 'created')

    def test_missing_store_id(self):
        self.response = self.client.post(
            '/api/v1/store/image', data={
                'image': '/files/testpic.jpg'
            })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreImageViews.as_view()(
            self.response)
        self.assertEqual(self.response.data, 'store id is required')

    def test_missing_image(self):
        self.response = self.client.post(
            '/api/v1/store/image', data={
                'store_id': self.mystore['id']
            })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreImageViews.as_view()(
            self.response)
        self.assertEqual(self.response.data, 'image is required')

    def test_not_login(self):
        self.response = self.client.post(
            '/api/v1/store/image')
        self.response = StoreViews.StoreImageViews.as_view()(
            self.response)
        self.assertEqual(self.response.data['detail'],
                         'Authentication credentials were not provided.')
