from rest_framework.test import APIRequestFactory, force_authenticate
from django.urls import resolve
from django.test import TestCase
from account import views as AccountViews
from account import models as AccountModels
from store import models as StoreModels
from store import views as StoreViews
from store import serializers


class StoreUpdateTestCase(TestCase):
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

    def test_url_name_store(self):
        resolver = resolve('/api/v1/store/update')
        self.assertEqual(resolver.view_name, 'store:update_store')

    def test_update_the_store_using_user1obj_update_name(self):
        self.response = self.client.post('/api/v1/store/update',
                                         {'store_id': self.mystore['id'], 'name': 'update my store', 'Account': self.user1Obj.id, 'address': 'cebu city', 'image': '/files/mystore_image.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreUpdateViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.data['status'], 'updated')
        self.assertEqual(
            self.response.data['store']['name'], 'update my store')

    def test_update_the_store_using_user1obj_update_address(self):
        self.response = self.client.post('/api/v1/store/update',
                                         {'store_id': self.mystore['id'], 'name': 'update my store', 'Account': self.user1Obj.id, 'address': 'update cebu city', 'image': '/files/mystore_image.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreUpdateViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.data['status'], 'updated')
        self.assertEqual(
            self.response.data['store']['address'], 'update cebu city')

    def test_update_the_store_using_user1obj_update_image(self):
        self.response = self.client.post('/api/v1/store/update',
                                         {'store_id': self.mystore['id'], 'name': 'update my store', 'Account': self.user1Obj.id, 'address': 'update cebu city', 'image': '/files/new_mystore_image.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreUpdateViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.data['status'], 'updated')
        self.assertEqual(
            self.response.data['store']['image'], '/files/new_mystore_image.jpg')

    def test_update_the_store_using_user1obj_missing_store_id(self):
        self.response = self.client.post('/api/v1/store/update',
                                         {'name': 'update my store', 'Account': self.user1Obj.id, 'address': 'update cebu city', 'image': '/files/new_mystore_image.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreUpdateViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(self.response.data, 'store id is required')

    def test_update_the_store_using_user1obj_missing_account(self):
        self.response = self.client.post('/api/v1/store/update',
                                         {'store_id': self.mystore['id'], 'name': 'update my store', 'address': 'update cebu city', 'image': '/files/new_mystore_image.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreUpdateViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(self.response.data, 'user id is required')

    def test_update_the_store_using_user1obj_missing_name(self):
        self.response = self.client.post('/api/v1/store/update',
                                         {'store_id': self.mystore['id'], 'Account': self.user1Obj.id, 'address': 'update cebu city', 'image': '/files/new_mystore_image.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreUpdateViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(
            self.response.data, 'store name is required')

    def test_update_the_store_using_user1obj_missing_address(self):
        self.response = self.client.post('/api/v1/store/update',
                                         {'store_id': self.mystore['id'], 'name': 'update my store', 'Account': self.user1Obj.id, 'image': '/files/new_mystore_image.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreUpdateViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(
            self.response.data, 'store address is required')

    def test_update_the_store_using_user1obj_missing_image(self):
        self.response = self.client.post('/api/v1/store/update',
                                         {'store_id': self.mystore['id'], 'name': 'update my store', 'Account': self.user1Obj.id, 'address': 'update cebu city'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreUpdateViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(
            self.response.data, 'store image is required')

    def test_not_login(self):
        self.response = self.client.post('/api/v1/store/update',
                                         {'store_id': self.mystore['id'], 'name': 'update my store', 'Account': self.user1Obj.id, 'address': 'update cebu city'})
        self.response = StoreViews.StoreUpdateViews.as_view()(self.response)

        self.assertEqual(self.response.data['detail'],
                         'Authentication credentials were not provided.')
