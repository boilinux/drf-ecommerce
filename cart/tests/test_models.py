from django.test import TestCase

from account.models import Account
from product.models import Product
from order.models import Order
from cart.models import LineItem
from store.models import Store
# Create your tests here.


class custom:
    def create_products():
        user1 = Account.objects.get(username='09499272761')
        store1 = Store.objects.create(
            Account=user1, name='store1', address='address1')
        Product.objects.create(
            Store=store1, title='product1', description='description1', price='99.9')
        Product.objects.create(
            Store=store1, title='product2', description='description2', price='10')
        Product.objects.create(
            Store=store1, title='product3', description='description3', price='11')
        Product.objects.create(
            Store=store1, title='product4', description='description4', price='12', stock=False, free_shipping=True)

    def get_products():
        myObj = []
        myObj.append(Product.objects.get(title='product1'))
        myObj.append(Product.objects.get(title='product2'))
        myObj.append(Product.objects.get(title='product3'))
        myObj.append(Product.objects.get(title='product4'))
        return myObj

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

    def create_orders():
        user1 = Account.objects.get(username='09499272761')
        user2 = Account.objects.get(username='09499272762')

        Order.objects.create(Account=user1, total='1500', datetime='2021-12-09T09:30:46.431995',
                             phone_number=user1.username, full_name='stephen wenceslao', address='address1')
        Order.objects.create(Account=user1, total='200', datetime='2021-11-09T09:30:46.431995',
                             phone_number=user1.username, full_name='stephen wenceslao', address='address1')

        Order.objects.create(Account=user2, total='100', datetime='2021-14-09T09:30:46.431995', phone_number=user2.username,
                             full_name='stephen wenceslao2', address='address2', notes='set time to 3mins', delivery_fee='50', status='processing')
        Order.objects.create(Account=user2, total='200', datetime='2021-13-09T09:30:46.431995', phone_number=user2.username,
                             full_name='stephen wenceslao2', address='address2', delivery_fee='80', status='delivered')

    def get_orders(user):
        return Order.objects.filter(Account=user)


class LineItemTestCase(TestCase):
    def setUp(self):
        custom.create_users()
        custom.create_products()
        custom.create_orders()

        userObj = custom.get_users()
        products = custom.get_products()
        user1Orders = custom.get_orders(userObj[0])
        user2Orders = custom.get_orders(userObj[1])
        counter = 0
        for index, thisProduct in enumerate(products):
            for index2, thisOrder in enumerate(user1Orders):
                counter += 1
                LineItem.objects.create(Order=thisOrder, Product=thisProduct, Account=userObj[0], title='order {} and product {} with orderId {}'.format(
                    thisOrder.phone_number, thisProduct.title, thisOrder.id), quantity=1, price='99')

        for index, thisProduct in enumerate(products):
            counter += 1
            LineItem.objects.create(Product=thisProduct, Account=userObj[0], title='order {} and product {}'.format(
                thisOrder.phone_number, thisProduct.title), quantity=1, price='99.1')

        for index, thisProduct in enumerate(products):
            for index2, thisOrder in enumerate(user2Orders):
                counter += 1
                LineItem.objects.create(Order=thisOrder, Product=thisProduct, Account=userObj[1], title='order {} and product {}'.format(
                    thisOrder.phone_number, thisProduct.title), quantity=2, price='999')

        for index, thisProduct in enumerate(products):
            counter += 1
            LineItem.objects.create(Product=thisProduct, Account=userObj[1], title='order {} and product {} with orderId {}'.format(
                thisOrder.phone_number, thisProduct.title, thisOrder.id), quantity=1, price='999.1')

        # print('line items created {}'.format(counter))

    def test_line_item(self):
        userObj = custom.get_users()
        user1LineItems = LineItem.objects.filter(Account=userObj[0])
        user2LineItems = LineItem.objects.filter(Account=userObj[1])

        counter = 0

        self.assertEqual(
            user1LineItems[0].title, 'order 09499272761 and product product1 with orderId 1')
        for thisLineItem in user1LineItems.iterator():
            counter += 1
            # print('title: {} ; lineitemID: {}'.format(
            #     thisLineItem.title, thisLineItem.id))
        self.assertEqual(user1LineItems[11].title,
                         'order 09499272761 and product product4')

        self.assertEqual(
            user2LineItems[0].title, 'order 09499272762 and product product1')
        for thisLineItem in user2LineItems.iterator():
            counter += 1
            # print('title: {} ; lineitemID: {}'.format(
            #     thisLineItem.title, thisLineItem.id))
        self.assertEqual(
            user2LineItems[11].title, 'order 09499272762 and product product4 with orderId 4')

        # print('line items existed {}'.format(counter))
        self.assertEqual(counter, 24)
