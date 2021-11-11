from django.test import TestCase

from account.models import Account
from product.models import Product
from order.models import Order
from cart.models import LineItem, LineItemImage
from store.models import Store


class LineItemImageTestCase(TestCase):
    def setUp(self):
        self.user1 = Account.objects.create(username='09499272761', password='password1', email='09499272761@localhost.local',
                                            full_name='stephen wenceslao', account_type=0)
        self.store1 = Store.objects.create(
            Account=self.user1, name='store1', address='address1')
        self.product1 = Product.objects.create(
            Store=self.store1, title='product8', description='description4', price='12', stock=False, free_shipping=True)

        self.lineitem1 = LineItem.objects.create(Account=self.user1, Product=self.product1, title='my lineitem 1',
                                                 description='this is a description for lineitem', price='99.11', quantity='5')

    def test_create_lineitem_image(self):
        self.lineItemImg = LineItemImage.objects.create(
            LineItem=self.lineitem1, image='/file/lineitem_image.jpg')

        self.assertIsNotNone(self.lineItemImg.id)
        self.assertEqual(self.lineItemImg.image, '/file/lineitem_image.jpg')
