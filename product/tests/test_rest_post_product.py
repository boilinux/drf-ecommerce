from rest_framework.test import APIRequestFactory, force_authenticate
from django.urls import reverse, resolve
from django.test import TestCase

from account import views as AccountViews
from account import models as AccountModels
from store import models as StoreModels
from store import views as StoreViews
from product import serializers
from product import models, views


class CreateProductTestCase(TestCase):
    def setUp(self):
        self.client = APIRequestFactory()
        self.response = self.client.post('/api/v1/account/register',
                                         {'username': '09499272112', 'password': 'password1', 'password2': 'password1', 'email': '09499272112@localhost.local', 'full_name': 'stephen wenceslao'})
        self.response = AccountViews.AccountRegisterViews.as_view()(self.response)
        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data['status'], 'created')

        self.response = self.client.post('/api/v1/account/login',
                                         {'username': '09499272112', 'password': 'password1'})
        self.response = AccountViews.AccountLoginViews.as_view()(self.response)
        self.userToken = self.response.data['token']

        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.data['status'], 'login')

        self.user1Obj = AccountModels.Account.objects.get(
            pk=self.response.data['user_info']['id'])
        self.assertEqual(self.user1Obj.username, '09499272112')

        self.response = self.client.post('/api/v1/store/create',
                                         {'name': 'my store 3', 'Account': self.user1Obj.id, 'address': 'cebu city', 'image': '/files/mystore_image.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = StoreViews.StoreCreateViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data['status'], 'created')
        self.storeObj = self.response.data['store']

        self.response = self.client.post('/api/v1/product',
                                         {'Store': self.storeObj['id'], 'title': 'Product A', 'description': 'description of product A', 'price': '99.99', 'image': '/file/product_a.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.ProductViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data, 'created')

    def test_url_name_product(self):
        resolver = resolve('/api/v1/product')
        self.assertEqual(resolver.view_name, 'product:post_put_delete_product')

    def test_create_product_not_login(self):
        self.response = self.client.post('/api/v1/product',
                                         {'Store': self.storeObj['id'], 'title': 'Product A', 'description': 'description of product A', 'price': '99.99', 'image': '/file/product_a.jpg'})
        self.response = views.ProductViews.as_view()(self.response)

        self.assertEqual(self.response.data['detail'],
                         'Authentication credentials were not provided.')

    def test_missing_store_id(self):
        self.response = self.client.post('/api/v1/product',
                                         {'title': 'Product A', 'description': 'description of product A', 'price': '99.99', 'image': '/file/product_a.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.ProductViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(self.response.data, 'Store id is required')

    def test_missing_title(self):
        self.response = self.client.post('/api/v1/product',
                                         {'Store': self.storeObj['id'], 'description': 'description of product A', 'price': '99.99', 'image': '/file/product_a.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.ProductViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(
            self.response.data, 'Product title is required')

    def test_missing_description(self):
        self.response = self.client.post('/api/v1/product',
                                         {'Store': self.storeObj['id'], 'title': 'Product A', 'price': '99.99', 'image': '/file/product_a.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.ProductViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(
            self.response.data, 'Product description is required')

    def test_missing_price(self):
        self.response = self.client.post('/api/v1/product',
                                         {'Store': self.storeObj['id'], 'title': 'Product A', 'description': 'description of product A', 'image': '/file/product_a.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.ProductViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(
            self.response.data, 'Product price is required')

    def test_missing_image(self):
        self.response = self.client.post('/api/v1/product',
                                         {'Store': self.storeObj['id'], 'title': 'Product A', 'description': 'description of product A', 'price': '99.99'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.ProductViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(
            self.response.data, 'Product image is required')

    def test_product_serializer(self):
        self.serializer = serializers.ProductSerializer(
            models.Product.objects.get(Store=self.storeObj['id'], title='Product A'))
        self.assertEqual(self.serializer.data, {
                         'id': self.serializer.data['id'], 'title': 'Product A', 'description': 'description of product A', 'price': '99.99', 'image': '/file/product_a.jpg', 'stock': True, 'free_shipping': False, 'Store': self.storeObj['id']})
