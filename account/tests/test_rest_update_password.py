from rest_framework.test import APIRequestFactory, force_authenticate
from django.urls import resolve
from django.test import TestCase
from account import views
from account.models import Account
from account.serializers import ChangePasswordSerializer


class AccountUpdatePasswordTestCase(TestCase):
    def setUp(self):
        resolver = resolve('/api/v1/account/register')
        self.assertEqual(resolver.view_name, 'account:register')

        client = APIRequestFactory()
        response = client.post('/api/v1/account/register',
                               {'username': '09499272710', 'password': 'password1', 'password2': 'password1', 'email': '09499272761@localhost.local', 'full_name': 'stephen wenceslao'})
        response = views.AccountRegisterViews.as_view()(response)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], 'created')

    def test_change_password_serializer(self):
        serializer = ChangePasswordSerializer(data={
            'old_password': 'password',
            'new_password': 'password2'
        })
        if serializer.is_valid():
            self.assertEqual(serializer.data['old_password'], 'password')
            self.assertEqual(serializer.data['new_password'], 'password2')
            self.assertEqual(
                serializer.data, {'old_password': 'password', 'new_password': 'password2'})

    def test_account_change_password(self):
        resolver = resolve('/api/v1/account/update/password')
        self.assertEqual(resolver.view_name, 'account:update_password')

        client = APIRequestFactory()

        response = client.post('/api/v1/account/login',
                               {'username': '09499272710', 'password': 'password1'})
        response = views.AccountLoginViews.as_view()(response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'login')
        self.assertIsNotNone(response.data['user_info'])
        userToken = response.data['token']
        userObj = Account.objects.get(
            username=response.data['user_info']['username'])

        response = client.post('/api/v1/account/update',
                               {'username': '09499272710', 'old_password': 'password', 'new_password': 'password2'})
        force_authenticate(response, user=userObj, token=userToken)
        response = views.AccountUpdatePasswordViews.as_view()(response)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, 'user not exist or old password is incorrect')

        response = client.post('/api/v1/account/update',
                               {'username': '09499272710', 'old_password': 'password', 'new_password': 'password'})
        force_authenticate(response, user=userObj, token=userToken)
        response = views.AccountUpdatePasswordViews.as_view()(response)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data, 'new password should not equal to new password')

        response = client.post('/api/v1/account/update',
                               {'username': '09499272710', 'old_password': 'password1', 'new_password': 'pass'})
        force_authenticate(response, user=userObj, token=userToken)
        response = views.AccountUpdatePasswordViews.as_view()(response)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data, 'new password should be greater than 5')

        response = client.post('/api/v1/account/update',
                               {'username': '0949927271', 'old_password': 'password1', 'new_password': 'newpassword'})
        force_authenticate(response, user=userObj, token=userToken)
        response = views.AccountUpdatePasswordViews.as_view()(response)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data, 'user not exist or old password is incorrect')

        response = client.post('/api/v1/account/update',
                               {'username': '09499272710', 'old_password': 'password1', 'new_password': 'newpassword'})
        force_authenticate(response, user=userObj, token=userToken)
        response = views.AccountUpdatePasswordViews.as_view()(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data, 'user password updated')

        response = client.post('/api/v1/account/update',
                               {'username': '09499272710', 'old_password': 'password1', 'new_password': 'newpassword'})
        response = views.AccountUpdatePasswordViews.as_view()(response)

        self.assertEqual(response.data['detail'],
                         'Authentication credentials were not provided.')
