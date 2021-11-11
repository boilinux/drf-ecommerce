from re import template
from django.http.request import HttpHeaders
from rest_framework.test import APIRequestFactory, force_authenticate
from django.urls import resolve
from django.test import TestCase
from account import views
import json

from account.models import Account


class AccountLogoutTestCase(TestCase):
    def setUp(self):
        resolver = resolve('/api/v1/account/register')
        self.assertEqual(resolver.view_name, 'account:register')

        client = APIRequestFactory()
        response = client.post('/api/v1/account/register',
                               {'username': '09499272768', 'password': 'password1', 'password2': 'password1', 'email': '09499272761@localhost.local', 'full_name': 'stephen wenceslao'})
        response = views.AccountRegisterViews.as_view()(response)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], 'created')

        resolver = resolve('/api/v1/account/login')
        self.assertEqual(resolver.view_name, 'account:login')

    def test_user_logout(self):
        resolver = resolve('/api/v1/account/logout')
        self.assertEqual(resolver.view_name, 'account:logout')

        client = APIRequestFactory()

        response = client.post('/api/v1/account/login',
                               {'username': '09499272768', 'password': 'password1'})
        response = views.AccountLoginViews.as_view()(response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'login')
        self.assertIsNotNone(response.data['user_info'])
        userToken = response.data['token']
        userObj = Account.objects.get(
            username=response.data['user_info']['username'])

        self.assertEqual(response.data['user_info']['username'], '09499272768')

        response = client.post('/api/v1/account/logout',
                               {'username': '09499272768', 'password': 'password'})
        response = views.AccountLogoutViews.as_view()(response)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.dumps(
            response.data), '{"detail": "Authentication credentials were not provided."}')

        response = client.post('/api/v1/account/logout',
                               data={'username': '09499272768', 'password': 'password'})

        force_authenticate(response, user=userObj, token=userToken)
        response = views.AccountLogoutViews.as_view()(response)
        self.assertEqual(response.status_code, 501)
        self.assertEqual(response.data, 'user does not exist')

        response = client.post('/api/v1/account/logout',
                               {'username': '09499272768', 'password': 'password1'})
        force_authenticate(response, user=userObj, token=userToken)
        response = views.AccountLogoutViews.as_view()(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'you are now logout')

        response = client.post('/api/v1/account/login',
                               {'username': '09499272768', 'password': 'password1'})
        response = views.AccountLoginViews.as_view()(response)
        self.assertNotEqual(userToken, response.data['token'])
