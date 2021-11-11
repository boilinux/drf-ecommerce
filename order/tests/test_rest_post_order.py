from rest_framework.test import APIRequestFactory, force_authenticate
from django.urls import reverse, resolve
from django.test import TestCase

from account import views as AccountViews
from account import models as AccountModels
from product import models as ProductModels, views as ProductViews
from order import serializers
from order import models
from order import views


class CreateOrderTestCase(TestCase):
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

    def test_url_name_order(self):
        resolver = resolve(
            '/api/v1/order')
        self.assertEqual(resolver.view_name, 'order:post_order')

    def test_product_serializer(self):
        order = models.Order.objects.create(
            Account=self.user1Obj, total='99.99', datetime='now', phone_number='09159524049', full_name='stephen wenceslao', address='camotes island', notes='my notes', delivery_fee='123', status='processing'
        )
        self.serializer = serializers.OrderSerializer(
            models.Order.objects.get(pk=order.id))

        self.assertIsNotNone(order.id)
        self.assertEqual(self.serializer.data['total'], '99.99')

    def test_create_order_base_on_user1_missing_user_id(self):
        self.response = self.client.post('/api/v1/order', {
            'total': '99.99', 'datetime': 'today', 'phone_number': '09159524049', 'full_name': 'stephen wenceslao', 'address': 'camotes island', 'notes': 'this is my notes', 'delivery_fee': '9.10', 'status': 'processing'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.OrderViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(
            self.response.data, 'User id is required')

    def test_create_order_base_on_user1_missing_full_name(self):
        self.response = self.client.post('/api/v1/order', {
            'Account': self.user1Obj.id, 'total': '99.99', 'datetime': 'today', 'phone_number': '09159524049', 'address': 'camotes island', 'notes': 'this is my notes', 'delivery_fee': '9.10', 'status': 'processing'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.OrderViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(
            self.response.data, 'Full name is required')

    def test_create_order_base_on_user1_missing_total(self):
        self.response = self.client.post('/api/v1/order', {
            'Account': self.user1Obj.id,  'datetime': 'today', 'phone_number': '09159524049', 'full_name': 'stephen wenceslao', 'address': 'camotes island', 'notes': 'this is my notes', 'delivery_fee': '9.10', 'status': 'processing'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.OrderViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(
            self.response.data, 'Total is required')

    def test_create_order_base_on_user1_missing_phone_number(self):
        self.response = self.client.post('/api/v1/order', {
            'Account': self.user1Obj.id, 'total': '99.99', 'datetime': 'today', 'full_name': 'stephen wenceslao', 'address': 'camotes island', 'notes': 'this is my notes', 'delivery_fee': '9.10', 'status': 'processing'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.OrderViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(
            self.response.data, 'Phone number is required')

    def test_create_order_base_on_user1_missing_datetime(self):
        self.response = self.client.post('/api/v1/order', {
            'Account': self.user1Obj.id, 'total': '99.99', 'phone_number': '09159524049', 'full_name': 'stephen wenceslao', 'address': 'camotes island', 'notes': 'this is my notes', 'delivery_fee': '9.10', 'status': 'processing'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.OrderViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(
            self.response.data, 'Datetime is required')

    def test_create_order_base_on_user1_missing_address(self):
        self.response = self.client.post('/api/v1/order', {
            'Account': self.user1Obj.id, 'total': '99.99', 'datetime': 'today', 'phone_number': '09159524049', 'full_name': 'stephen wenceslao', 'notes': 'this is my notes', 'delivery_fee': '9.10', 'status': 'processing'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.OrderViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(
            self.response.data, 'Address is required')

    def test_create_order_base_on_user1_missing_notes_is_ok(self):
        self.response = self.client.post('/api/v1/order', {
            'Account': self.user1Obj.id, 'total': '99.99', 'datetime': 'today', 'phone_number': '09159524049', 'full_name': 'stephen wenceslao', 'address': 'camotes island', 'delivery_fee': '9.10', 'status': 'processing'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.OrderViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(
            self.response.data, 'created')

    def test_create_order_base_on_user1_missing_delivery_fee_is_ok(self):
        self.response = self.client.post('/api/v1/order', {
            'Account': self.user1Obj.id, 'total': '99.99', 'datetime': 'today', 'phone_number': '09159524049', 'full_name': 'stephen wenceslao', 'address': 'camotes island', 'notes': 'this is my notes', 'status': 'processing'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.OrderViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(
            self.response.data, 'created')

    def test_create_order_base_on_user1_missing_status_is_ok(self):
        self.response = self.client.post('/api/v1/order', {
            'Account': self.user1Obj.id, 'total': '99.99', 'datetime': 'today', 'phone_number': '09159524049', 'full_name': 'stephen wenceslao', 'address': 'camotes island', 'notes': 'this is my notes', 'delivery_fee': '9.10'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.OrderViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(
            self.response.data, 'created')

    def test_create_order_base_on_user1(self):
        self.response = self.client.post('/api/v1/order', {
            'Account': self.user1Obj.id, 'total': '99.99', 'datetime': 'today', 'phone_number': '09111111111', 'full_name': 'stephen wenceslao', 'address': 'camotes island', 'notes': 'this is my notes', 'delivery_fee': '9.10', 'status': 'processing'
        })
        force_authenticate(self.response, user=self.user1Obj,
                           token=self.userToken)
        self.response = views.OrderViews.as_view()(self.response)

        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(
            self.response.data, 'created')

        order = models.Order.objects.get(phone_number='09111111111')
        self.assertEqual(order.phone_number, '09111111111')
