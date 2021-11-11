from rest_framework.test import APIRequestFactory, RequestsClient
from django.urls import reverse, resolve
from django.test import TestCase
from account import views

from account.models import Account
from account.serializers import AccountSerializer, AccountRegistrationSerializer
import json


class AccountRegisterTestCase(TestCase):
    def test_register(self):
        resolver = resolve('/api/v1/account/register')
        self.assertEqual(resolver.view_name, 'account:register')

        client = APIRequestFactory()
        response = client.post('/api/v1/account/register',
                               {'username': '09499272761', 'password': 'password1', 'password2': 'password1', 'email': '09499272761@localhost.local', 'full_name': 'stephen wenceslao'})
        response = views.AccountRegisterViews.as_view()(response)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], 'created')
        self.assertIsNotNone(response.data['token'])
        self.assertNotEqual(response.data['token'], '')

        response = client.post('/api/v1/account/register',
                               {'username': '01499272761', 'password': 'password1'})
        response = views.AccountRegisterViews.as_view()(response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data, 'Invalid Phone Number, should start in 09')

        response = client.post('/api/v1/account/register',
                               {'username': '', 'password': 'password1'})
        response = views.AccountRegisterViews.as_view()(response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data, 'Phone Number field is required.')

        response = client.post('/api/v1/account/register',
                               {'username': '09', 'password': 'password1'})
        response = views.AccountRegisterViews.as_view()(response)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data, 'Phone Number should be 11 digit 09xxxxxxxxx.')

        response = client.post('/api/v1/account/register',
                               {'password': 'password1', 'password2': 'password1', 'email': '09499272761@localhost.local', 'full_name': 'stephen wenceslao'})
        response = views.AccountRegisterViews.as_view()(response)

        self.assertEqual(response.status_code, 501)
        self.assertEqual(response.data, 'error')


class AccountSerializerTestCase(TestCase):
    def setUp(self):
        Account.objects.create(username='09499272761', password='password1', email='09499272761@localhost.local',
                               full_name='stephen wenceslao', account_type=0)
        Account.objects.create(username='09499272762', password='password2', email='09499272762@localhost.local',
                               full_name='stephen wenceslao2', account_type=1)

    def test_account_serializer(self):
        user1 = Account.objects.get(username='09499272761')
        user2 = Account.objects.get(username='09499272762')

        serializer = AccountSerializer(user1)
        self.assertEqual(
            serializer.data['username'], '09499272761')

        serializer = AccountSerializer(user2)
        self.assertEqual(
            serializer.data['username'], '09499272762')


class AccountRegistrationSerializerTestCase(TestCase):
    def setUp(self):
        data = {
            'username': '09499272769',
            'password': 'password',
            'password2': 'password',
            'email': '09499272769@localhost.local',
            'full_name': 'stephen wenceslao'
        }

        serializer = AccountRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

    def test_registration_serializer(self):
        user1 = Account.objects.get(username='09499272769')

        serializer = AccountSerializer(user1)
        self.assertEqual(serializer.data['username'], '09499272769')
        self.assertEqual(serializer.data['email'],
                         '09499272769@localhost.local')


class ReceivedSMSRegistrationTestCase(TestCase):
    pass
