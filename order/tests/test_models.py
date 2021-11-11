from django.test import TestCase
from order.models import Order
from account.models import Account

# Create your tests here.


class custom:
    def create_users():
        Account.objects.create(username='09499272761', password='password1', email='09499272761@localhost.local',
                               full_name='stephen wenceslao', account_type=0)
        Account.objects.create(username='09499272762', password='password2', email='09499272762@localhost.local',
                               full_name='stephen wenceslao2', account_type=1)

    def get_users():
        return [
            Account.objects.get(username='09499272761'),
            Account.objects.get(username='09499272762'),
        ]


class OrderTestCase(TestCase):
    def setUp(self):
        custom.create_users()
        userObj = custom.get_users()

        Order.objects.create(Account=userObj[0], total='1500', datetime='2021-12-09T09:30:46.431995',
                             phone_number=userObj[0].username, full_name='stephen wenceslao', address='address1')
        Order.objects.create(Account=userObj[0], total='200', datetime='2021-11-09T09:30:46.431995',
                             phone_number=userObj[0].username, full_name='stephen wenceslao', address='address1')

        Order.objects.create(Account=userObj[1], total='100', datetime='2021-14-09T09:30:46.431995', phone_number=userObj[0].username,
                             full_name='stephen wenceslao2', address='address2', notes='set time to 3mins', delivery_fee='50', status='processing')
        Order.objects.create(Account=userObj[1], total='200', datetime='2021-13-09T09:30:46.431995', phone_number=userObj[0].username,
                             full_name='stephen wenceslao2', address='address2', delivery_fee='80', status='delivered')

    def test_order(self):
        userObj = custom.get_users()
        user1Orders = Order.objects.filter(Account=userObj[0])
        user2Orders = Order.objects.filter(Account=userObj[1])

        for thisOrder in user1Orders.iterator():
            self.assertEqual(thisOrder.address, 'address1')

        for thisOrder in user2Orders.iterator():
            self.assertEqual(thisOrder.address, 'address2')

        orderObj = Order.objects
        self.assertEqual(orderObj.get(
            Account=userObj[0], total='1500').total, '1500')
        self.assertEqual(orderObj.get(
            Account=userObj[0], total='200').total, '200')

        self.assertEqual(orderObj.get(
            Account=userObj[1], total='200').status, 'delivered')
