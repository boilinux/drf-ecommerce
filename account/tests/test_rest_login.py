from rest_framework.test import APIRequestFactory
from django.urls import resolve
from django.test import TestCase
from account import views


class AccountLoginTestCase(TestCase):
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

    def test_account_login(self):
        client = APIRequestFactory()

        response = client.post('/api/v1/account/login',
                               {'username': '09499272760', 'password': 'passw'})
        response = views.AccountLoginViews.as_view()(response)

        self.assertEqual(response.status_code, 501)
        self.assertEqual(response.data, 'username does not exist')

        response = client.post('/api/v1/account/login',
                               {'username': '09499272768', 'password': 'password1'})
        response = views.AccountLoginViews.as_view()(response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'login')
        self.assertNotEqual(response.data['user_info'], '')
        self.assertNotEqual(response.data['token'], '')
