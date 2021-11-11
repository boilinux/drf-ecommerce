from django.test import TestCase
from rest_framework.authtoken.models import Token
from account.models import Account

# Create your tests here.


class AccountTestCase(TestCase):
    def setUp(self):
        Account.objects.create(username='09499272761', password='password1', email='09499272761@localhost.local',
                               full_name='stephen wenceslao', account_type=0)
        Account.objects.create(username='09499272762', password='password2', email='09499272762@localhost.local',
                               full_name='stephen wenceslao2', account_type=1)

    def test_account(self):
        user1 = Account.objects.get(username='09499272761')
        user2 = Account.objects.get(username='09499272762')
        token, created = Token.objects.get_or_create(user=user1)
        token2, created2 = Token.objects.get_or_create(user=user2)

        # print('user1 token is {} created {}'.format(token.key, created))
        # print('user2 token is {} created {}'.format(token2.key, created2))

        self.assertIsNotNone(token.key)
        self.assertIsNotNone(token2.key)

        self.assertEqual(user1.email, '09499272761@localhost.local')
        self.assertEqual(user2.email, '09499272762@localhost.local')

        self.assertEqual(user1.account_type, 0)
        self.assertEqual(user2.account_type, 1)

        self.assertEqual(user1.username, '09499272761')
        self.assertEqual(user2.username, '09499272762')

        self.assertEqual(user1.profile_image, '')
        self.assertEqual(user2.profile_image, '')

        self.assertEqual(user1.is_admin, False)
        self.assertEqual(user2.is_admin, 0)

        self.assertEqual(user1.password, 'password1')
        self.assertEqual(user2.password, 'password2')

        self.assertEqual(user1.full_name, 'stephen wenceslao')
        self.assertEqual(user2.full_name, 'stephen wenceslao2')

        self.assertEqual(user1.password, 'password1')
        self.assertEqual(user2.password, 'password2')
