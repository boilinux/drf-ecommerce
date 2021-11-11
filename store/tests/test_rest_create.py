from rest_framework.test import APIRequestFactory, force_authenticate
from django.urls import resolve
from django.test import TestCase
from account import views as AccountViews
from account import models as AccountModels
from store import models as StoreModels
from store import views as StoreViews
from store import serializers


class StoreCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIRequestFactory()
        self.response = self.client.post('/api/v1/account/register',
                                         {'username': '09499272712', 'password': 'password1', 'password2': 'password1', 'email': '09499272761@localhost.local', 'full_name': 'stephen wenceslao'})
        self.response = AccountViews.AccountRegisterViews.as_view()(self.response)
        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data['status'], 'created')

        self.response = self.client.post('/api/v1/account/login',
                                         {'username': '09499272712', 'password': 'password1'})
        self.response = AccountViews.AccountLoginViews.as_view()(self.response)
        self.userToken = self.response.data['token']

        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.data['status'], 'login')

        self.user1Obj = AccountModels.Account.objects.get(
            pk=self.response.data['user_info']['id'])
        self.assertEqual(self.user1Obj.username, '09499272712')

    def test_url_name_store(self):
        resolver = resolve('/api/v1/store/create')
        self.assertEqual(resolver.view_name, 'store:create_store')

    def test_store_create_serializer(self):
        self.store1Serializer = serializers.StoreSerializer(StoreModels.Store.objects.create(
            Account=self.user1Obj, name='my store name', address='my address', image='files/testpic.jpg'))
        self.assertEqual(self.store1Serializer.data, {
                         'id': self.store1Serializer.data['id'], 'name': 'my store name', 'address': 'my address', 'image': '/files/testpic.jpg', 'active': True, 'Account': self.user1Obj.id})

    def test_create_a_store_using_user1obj(self):
        self.response = self.client.post('/api/v1/store/create',
                                         {'name': 'my store', 'Account': self.user1Obj.id, 'address': 'cebu city', 'image': '/files/mystore_image.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreCreateViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data['status'], 'created')

    def test_create_a_store_using_user1obj_name_isrequired(self):
        self.response = self.client.post('/api/v1/store/create',
                                         {'name': '', 'Account': self.user1Obj.id, 'address': 'cebu city', 'image': '/files/mystore_image.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreCreateViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(self.response.data, 'store name is required')

    def test_create_a_store_using_user1obj_address_isrequired(self):
        self.response = self.client.post('/api/v1/store/create',
                                         {'name': 'my store', 'Account': self.user1Obj.id, 'address': '', 'image': '/files/mystore_image.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreCreateViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(self.response.data, 'store address is required')

    def test_create_a_store_using_user1obj_image_isrequired(self):
        self.response = self.client.post('/api/v1/store/create',
                                         {'name': 'my store', 'Account': self.user1Obj.id, 'address': 'cebu city', 'image': ''})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreCreateViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(self.response.data, 'store image is required')

    def test_not_login(self):
        self.response = self.client.post('/api/v1/store/create',
                                         {'name': 'my store', 'Account': self.user1Obj.id, 'address': 'cebu city', 'image': ''})
        self.response = StoreViews.StoreCreateViews.as_view()(self.response)

        self.assertEqual(self.response.data['detail'],
                         'Authentication credentials were not provided.')
