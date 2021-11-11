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


class DeleteCartItemTestCase(TestCase):
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
                                         {'Store': self.storeObj['id'], 'title': 'Product lineitem3', 'description': 'description of product lineitem1', 'price': '99.99', 'image': '/file/product_lineitem1.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = productViews.ProductViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data, 'created')

        self.response = self.client.post('/api/v1/product',
                                         {'Store': self.storeObj['id'], 'title': 'Product lineitem4', 'description': 'description of product lineitem2', 'price': '1300', 'image': '/file/product_lineitem1.jpg'})
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = productViews.ProductViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data, 'created')

        self.product1 = productModels.Product.objects.get(
            title='Product lineitem3')
        self.assertEqual(self.product1.description,
                         'description of product lineitem1')

        self.product2 = productModels.Product.objects.get(
            title='Product lineitem4')
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

        # product2 price is 1300
        self.response = self.client.post('/api/v1/cart', {
            'Account': self.user1Obj.id, 'Product': self.product2.id, 'title': 'lineitem1 title111111111111222222', 'description': 'my descriptionmy descriptionmy description', 'quantity': '1'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.CartViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data,
                         'created')

        self.item1 = models.LineItem.objects.get(
            title='lineitem1 title111111111111222222')
        self.assertEqual(self.item1.description,
                         'my descriptionmy descriptionmy description')
        self.assertEqual(self.item1.price, '1300.00')

        self.response = self.client.post('/api/v1/cart', {
            'Account': self.user1Obj.id, 'Product': self.product2.id, 'title': 'lineitem1 title111111111111222222', 'description': 'my descriptionmy descriptionmy description', 'quantity': '1'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.CartViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.data,
                         'cart item updated')

        self.response = self.client.post('/api/v1/cart', {
            'Account': self.user1Obj.id, 'Product': self.product2.id, 'title': 'lineitem1 title111111111111222222', 'description': 'my descriptionmy descriptionmy description', 'quantity': '1'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.CartViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.data,
                         'cart item updated')

        self.item1 = models.LineItem.objects.get(
            title='lineitem1 title111111111111222222')
        self.assertEqual(self.item1.quantity,
                         '3')
        self.assertEqual(self.item1.price,
                         '3900.00')

    def test_url_name_cart(self):
        resolver = resolve('/api/v1/cart')
        self.assertEqual(resolver.view_name, 'cart:post_delete_cart')

    def test_delete_cart_not_login(self):
        self.response = self.client.delete(
            '/api/v1/cart/{}'.format(self.item1.id))
        self.response = views.CartViews.as_view()(self.response, pk=self.item1.id)

        self.assertEqual(self.response.data['detail'],
                         'Authentication credentials were not provided.')

    def test_delete_cart_item_login(self):
        self.response = self.client.delete(
            '/api/v1/cart/{}'.format(self.item1.id))
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.CartViews.as_view()(self.response, pk=self.item1.id)

        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.data,
                         'cart item deleted')

        try:
            models.LineItem.objects.get(pk=self.item1.id)
            raise ValueError('cart item was not deleted')
        except models.LineItem.DoesNotExist:
            pass

    def test_cart_item_not_found(self):
        self.response = self.client.delete(
            '/api/v1/cart/{}'.format(1234))
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.CartViews.as_view()(self.response, pk=1234)

        self.assertEqual(self.response.status_code, 404)
        self.assertEqual(self.response.data,
                         'cart item not found')
