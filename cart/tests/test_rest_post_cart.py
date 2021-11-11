from rest_framework.test import APIRequestFactory, force_authenticate
from django.urls import reverse, resolve
from django.test import TestCase

from account import views as AccountViews
from account import models as AccountModels
from store import models as StoreModels
from store import views as StoreViews
from cart import serializers
from product import models as productModels, views as productViews
from cart import models, views
from order import views as orderViews, models as orderModels


class AddCartTestCase(TestCase):
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
                                         {'Store': self.storeObj['id'], 'title': 'Product lineitem1', 'description': 'description of product lineitem1', 'price': '99.99', 'image': '/file/product_lineitem1.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = productViews.ProductViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data, 'created')

        self.response = self.client.post('/api/v1/product',
                                         {'Store': self.storeObj['id'], 'title': 'Product lineitem2', 'description': 'description of product lineitem2', 'price': '12.99', 'image': '/file/product_lineitem1.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = productViews.ProductViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data, 'created')

        self.product1 = productModels.Product.objects.get(
            title='Product lineitem1')
        self.assertEqual(self.product1.description,
                         'description of product lineitem1')

        self.product2 = productModels.Product.objects.get(
            title='Product lineitem2')
        self.assertEqual(self.product2.description,
                         'description of product lineitem2')

        self.response = self.client.post('/api/v1/order', {
            'Account': self.user1Obj.id, 'total': '99.99', 'datetime': 'today', 'phone_number': '09111111111', 'full_name': 'stephen wenceslao', 'address': 'camotes island', 'notes': 'this is my notes', 'delivery_fee': '9.10', 'status': 'processing'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = orderViews.OrderViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(
            self.response.data, 'created')

        self.order1 = orderModels.Order.objects.get(
            Account=self.user1Obj.id, phone_number='09111111111')
        self.assertIsNotNone(self.order1.id)

    def test_url_name_cart(self):
        resolver = resolve('/api/v1/cart')
        self.assertEqual(resolver.view_name, 'cart:post_delete_cart')

    def test_create_cart_not_login(self):
        self.response = self.client.post('/api/v1/cart', {
            'Account': self.user1Obj.id, 'Product': self.product1.id, 'title': 'lineitem1 title', 'description': 'my description', 'price': '999', 'quantity': '10'
        })
        self.response = views.CartViews.as_view()(self.response)

        self.assertEqual(self.response.data['detail'],
                         'Authentication credentials were not provided.')

    def test_cart_serializer(self):
        self.serializer = serializers.CartSerializer(
            models.LineItem.objects.create(
                Account=self.user1Obj, Product=self.product1, title='Lineitem for serializer', price='99.99', quantity='5'
            ))
        self.assertEqual(self.serializer.data, {'id': self.serializer.data['id'], 'title': 'Lineitem for serializer',
                         'description': '', 'price': '99.99', 'quantity': '5', 'Account': self.user1Obj.id, 'Product': self.product1.id, 'Order': None})

    def test_create_missing_user_id(self):
        self.response = self.client.post('/api/v1/cart', {
            'Product': self.product1.id, 'title': 'lineitem1 title', 'description': 'my description', 'price': '999', 'quantity': '10'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.CartViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(self.response.data,
                         'User id is required')

    def test_create_missing_product_id(self):
        self.response = self.client.post('/api/v1/cart', {
            'Account': self.user1Obj.id, 'title': 'lineitem1 title', 'description': 'my description', 'price': '999', 'quantity': '10'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.CartViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(self.response.data,
                         'Product id is required')

    def test_create_missing_order_should_not_exist(self):
        self.response = self.client.post('/api/v1/cart', {
            'Account': self.user1Obj.id, 'Product': self.product1.id, 'Order': '1', 'title': 'lineitem1 title', 'description': 'my description', 'price': '999', 'quantity': '10'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.CartViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(self.response.data,
                         'Order is not required')

    def test_create_missing_title(self):
        self.response = self.client.post('/api/v1/cart', {
            'Account': self.user1Obj.id, 'Product': self.product1.id, 'description': 'my description', 'price': '999', 'quantity': '10'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.CartViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(self.response.data,
                         'Title is required')

    def test_create_missing_description(self):
        self.response = self.client.post('/api/v1/cart', {
            'Account': self.user1Obj.id, 'Product': self.product1.id, 'title': 'lineitem1 title', 'price': '999', 'quantity': '10'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.CartViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(self.response.data,
                         'Description is required')

    def test_create_price_is_present_not_ok(self):
        self.response = self.client.post('/api/v1/cart', {
            'Account': self.user1Obj.id, 'Product': self.product1.id, 'title': 'lineitem1 title', 'description': 'my description', 'quantity': '10', 'price': '123'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.CartViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(self.response.data,
                         'Price is not required because its auto update')

    def test_create_missing_quantity(self):
        self.response = self.client.post('/api/v1/cart', {
            'Account': self.user1Obj.id, 'Product': self.product1.id, 'title': 'lineitem1 title', 'description': 'my description'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.CartViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(self.response.data,
                         'Quantity is required')

    def test_create_lineitem_without_order_and_check_quantity_if_updated_and_price(self):
        # product2 price is 12.99
        self.response = self.client.post('/api/v1/cart', {
            'Account': self.user1Obj.id, 'Product': self.product2.id, 'title': 'lineitem1 title111111111111', 'description': 'my descriptionmy descriptionmy description', 'quantity': '20'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.CartViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data,
                         'created')

        self.item1 = models.LineItem.objects.get(
            title='lineitem1 title111111111111')
        self.assertEqual(self.item1.description,
                         'my descriptionmy descriptionmy description')
        self.assertEqual(self.item1.price, '12.99')

        self.response = self.client.post('/api/v1/cart', {
            'Account': self.user1Obj.id, 'Product': self.product2.id, 'title': 'lineitem1 title111111111111', 'description': 'my descriptionmy descriptionmy description', 'quantity': '10'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.CartViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.data,
                         'cart item updated')

        self.response = self.client.post('/api/v1/cart', {
            'Account': self.user1Obj.id, 'Product': self.product2.id, 'title': 'lineitem1 title111111111111', 'description': 'my descriptionmy descriptionmy description', 'quantity': '10'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.CartViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.data,
                         'cart item updated')

        self.item1 = models.LineItem.objects.get(
            title='lineitem1 title111111111111')
        self.assertEqual(self.item1.quantity,
                         '40')
        self.assertEqual(self.item1.price,
                         '519.60')

    def test_create_lineitem_something_went_wrong(self):
        self.response = self.client.post('/api/v1/cart', {
            'Account': 12333, 'test123123': '123123123', 'Product': self.product1.id, 'title': 'lineitem1 title', 'description': 'my description', 'quantity': '10'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.CartViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 500)
        self.assertEqual(self.response.data,
                         'something went wrong')
