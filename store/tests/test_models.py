from django.test import TestCase

from account.models import Account
from store.models import Store, StoreImage

# Create your tests here.


class StoreTestCase(TestCase):
    def setUp(self):
        # create account
        user1 = Account.objects.create(username='09499272761', password='password1', email='09499272761@localhost.local',
                                       full_name='stephen wenceslao', account_type=0)
        user2 = Account.objects.create(username='09499272762', password='password2', email='09499272762@localhost.local',
                                       full_name='stephen wenceslao2', account_type=1)

        Store.objects.create(
            Account=user1, name='store1', address='address1')
        Store.objects.create(
            Account=user2, name='store2', address='address2')

    def test_values_store(self):
        user1 = Account.objects.get(
            username='09499272761', password='password1')
        user2 = Account.objects.get(
            username='09499272762', password='password2')
        store1 = Store.objects.get(Account=user1)
        store2 = Store.objects.get(Account=user2)

        self.assertEqual(store1.name, 'store1')
        self.assertEqual(store2.name, 'store2')

        self.assertEqual(store1.address, 'address1')
        self.assertEqual(store2.address, 'address2')

        self.assertEqual(user1.username, '09499272761')
        self.assertEqual(user2.username, '09499272762')

        self.assertEqual(user1.password, 'password1')
        self.assertEqual(user2.password, 'password2')


class StoreImageTestCase(TestCase):
    def setUp(self):
        # create accounts
        user1 = Account.objects.create(username='09499222761', password='password1', email='09499222761@localhost.local',
                                       full_name='stephen wenceslao', account_type=0)
        user2 = Account.objects.create(username='09499222762', password='password2', email='09499222762@localhost.local',
                                       full_name='stephen wenceslao2', account_type=1)
        # create stores
        store1 = Store.objects.create(
            Account=user1, name='09499222761 store1', address='address1')
        store2 = Store.objects.create(
            Account=user2, name='09499222762 store2', address='address2')

        StoreImage.objects.create(Store=store1, image='/files/store1_0.png')
        StoreImage.objects.create(Store=store1, image='/files/store1_1.png')
        StoreImage.objects.create(Store=store1, image='/files/store1_2.png')
        StoreImage.objects.create(Store=store1, image='/files/store1_3.png')

        StoreImage.objects.create(Store=store2, image='/files/store2_0.png')
        StoreImage.objects.create(Store=store2, image='/files/store2_1.png')
        StoreImage.objects.create(Store=store2, image='/files/store2_2.png')
        StoreImage.objects.create(Store=store2, image='/files/store2_3.png')
        StoreImage.objects.create(Store=store2, image='/files/store2_4.png')
        StoreImage.objects.create(Store=store2, image='/files/store2_5.png')
        StoreImage.objects.create(Store=store2, image='/files/store2_6.png')
        StoreImage.objects.create(Store=store2, image='/files/store2_7.png')

    def test_store_images(self):
        store1 = Store.objects.get(name='09499222761 store1')
        store2 = Store.objects.get(name='09499222762 store2')
        store1Images = StoreImage.objects.filter(Store=store1).order_by('id')
        store2Images = StoreImage.objects.filter(Store=store2).order_by('id')

        for index, thisImage in enumerate(store1Images):
            self.assertEqual(
                thisImage.image, '/files/store{}_{}.png'.format(1, index))

        for index, thisImage in enumerate(store2Images):
            self.assertEqual(
                thisImage.image, '/files/store{}_{}.png'.format(2, index))
