from django.test import TestCase

from product.models import Favorites, ProductImage, Product, ProductReview
from account.models import Account
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

    def create_favorites(user, product, isfavorite):
        Favorites.objects.create(
            Account=user, Product=product, isfavorite=isfavorite)

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

    def create_orders(user):
        Order.objects.create(Account=user[0], total='1500', datetime='2021-12-09T09:30:46.431995',
                             phone_number=user[0].username, full_name='stephen wenceslao', address='address1')
        Order.objects.create(Account=user[0], total='200', datetime='2021-11-09T09:30:46.431995',
                             phone_number=user[0].username, full_name='stephen wenceslao', address='address1')

        Order.objects.create(Account=user[1], total='100', datetime='2021-14-09T09:30:46.431995', phone_number=user[1].username,
                             full_name='stephen wenceslao2', address='address2', notes='set time to 3mins', delivery_fee='50', status='processing')
        Order.objects.create(Account=user[1], total='200', datetime='2021-13-09T09:30:46.431995', phone_number=user[1].username,
                             full_name='stephen wenceslao2', address='address2', delivery_fee='80', status='delivered')

    def get_orders(user):
        return Order.objects.filter(Account=user)


class ProductTestCase(TestCase):
    def setUp(self):
        custom.create_users()
        custom.create_products()

    def test_product(self):
        obj = custom.get_products()
        # print(obj)
        product1 = obj[0]
        product2 = obj[1]
        product3 = obj[2]
        product4 = obj[3]

        self.assertEqual(product1.title, 'product1')
        self.assertEqual(product2.title, 'product2')
        self.assertEqual(product3.title, 'product3')

        self.assertEqual(product1.description, 'description1')
        self.assertEqual(product2.description, 'description2')
        self.assertEqual(product3.description, 'description3')

        self.assertEqual(product1.price, '99.9')
        self.assertEqual(product2.price, '10')
        self.assertEqual(product3.price, '11')

        self.assertEqual(product1.stock, True)
        self.assertEqual(product2.stock, True)
        self.assertEqual(product3.stock, True)

        self.assertEqual(product1.free_shipping, False)
        self.assertEqual(product2.free_shipping, False)
        self.assertEqual(product3.free_shipping, False)

        self.assertEqual(product4.stock, False)
        self.assertEqual(product4.free_shipping, True)


class FavoritesTestCase(TestCase):
    def setUp(self):
        # create account
        user1 = Account.objects.create(username='09499272761', password='password1', email='09499272761@localhost.local',
                                       full_name='stephen wenceslao', account_type=0)
        user2 = Account.objects.create(username='09499272762', password='password2', email='09499272762@localhost.local',
                                       full_name='stephen wenceslao2', account_type=1)

        custom.create_products()
        products = custom.get_products()
        custom.create_favorites(user1, products[0], True)
        custom.create_favorites(user1, products[1], False)
        custom.create_favorites(user1, products[2], True)
        custom.create_favorites(user1, products[3], False)

        custom.create_favorites(user2, products[0], False)
        custom.create_favorites(user2, products[1], True)
        custom.create_favorites(user2, products[2], False)
        custom.create_favorites(user2, products[3], True)

    def test_favorites(self):
        userObj = custom.get_users()
        self.assertEqual(userObj[0].username, '09499272761')
        self.assertEqual(userObj[1].username, '09499272762')

        user1Favorites = Favorites.objects.filter(Account=userObj[0])
        user1Fav = [True, False, True, False]
        user2Favorites = Favorites.objects.filter(Account=userObj[1])
        user2Fav = [False, True, False, True]

        products = custom.get_products()

        for index, thisFav in enumerate(user1Favorites):
            self.assertEqual(thisFav.Account.username, '09499272761')
            self.assertEqual(thisFav.Product, products[index])
            self.assertEqual(thisFav.isfavorite, user1Fav[index])

        for index, thisFav in enumerate(user2Favorites):
            self.assertEqual(thisFav.Account.username, '09499272762')
            self.assertEqual(thisFav.Product, products[index])
            self.assertEqual(thisFav.isfavorite, user2Fav[index])


class ProductImageTestCase(TestCase):
    def setUp(self):
        custom.create_users()
        custom.create_products()
        products = custom.get_products()
        for index in range(20):
            for i, thisProduct in enumerate(products):
                ProductImage.objects.create(
                    Product=thisProduct, image='/files/product/product_image_{}_{}.jpg'.format(i, index))

    def test_product_images(self):
        products = custom.get_products()
        for index in range(20):
            for i, thisProduct in enumerate(products):
                obj = ProductImage.objects.get(
                    Product=thisProduct, image='/files/product/product_image_{}_{}.jpg'.format(i, index))
                self.assertEqual(
                    obj.image, '/files/product/product_image_{}_{}.jpg'.format(i, index))
                self.assertEqual(obj.Product, thisProduct)


class ProductReviewTestCase(TestCase):
    def setUp(self):
        custom.create_users()
        custom.create_products()
        products = custom.get_products()
        userObj = custom.get_users()
        custom.create_orders(userObj)
        user1Orders = custom.get_orders(userObj[0])
        user2Orders = custom.get_orders(userObj[1])

        # create line items
        counter = 0
        for index, thisProduct in enumerate(products):
            for index2, thisOrder in enumerate(user1Orders):
                counter += 1
                LineItem.objects.create(Order=thisOrder, Product=thisProduct, Account=userObj[0], title='order {} and product {} with orderId {} and status is {}'.format(
                    thisOrder.phone_number, thisProduct.title, thisOrder.id, thisOrder.status), quantity=1, price='99')

        for index, thisProduct in enumerate(products):
            counter += 1
            LineItem.objects.create(Product=thisProduct, Account=userObj[0], title='order {} and product {}'.format(
                'null', thisProduct.title), quantity=1, price='99.1')

        for index, thisProduct in enumerate(products):
            for index2, thisOrder in enumerate(user2Orders):
                counter += 1
                LineItem.objects.create(Order=thisOrder, Product=thisProduct, Account=userObj[1], title='order {} and product {} and status is {}'.format(
                    thisOrder.phone_number, thisProduct.title, thisOrder.status), quantity=2, price='999')

        for index, thisProduct in enumerate(products):
            counter += 1
            LineItem.objects.create(Product=thisProduct, Account=userObj[1], title='order {} and product {}'.format(
                'null', thisProduct.title), quantity=1, price='999.1')

        ordersDelivered = Order.objects.filter(status='delivered')
        # print('-----------------------------create reviews for order with delivered status')
        for thisOrder in ordersDelivered.iterator():
            orderLineItems = LineItem.objects.filter(Order=thisOrder)
            for thisLineItem in orderLineItems.iterator():
                ProductReview.objects.create(Product=thisLineItem.Product, Account=thisLineItem.Account, Order=thisOrder,
                                             rating=5, comment='lineItem id is {}'.format(thisLineItem.id), datetime='now')

    def test_product_reviews_baseon_status_delivered_in_order(self):
        userObj = custom.get_users()
        user1LineItems = LineItem.objects.filter(Account=userObj[0])
        user2LineItems = LineItem.objects.filter(Account=userObj[1])

        counter = 0
        lineItems = []
        for thisLineItem in user1LineItems.iterator():
            counter += 1
            # print('title: {} ; lineitemID: {}'.format(
            #     thisLineItem.title, thisLineItem.id))
            if 'delivered' in thisLineItem.title:
                lineItems.append(thisLineItem.id)

        for thisLineItem in user2LineItems.iterator():
            counter += 1
            # print('title: {} ; lineitemID: {}'.format(
            #     thisLineItem.title, thisLineItem.id))
            if 'delivered' in thisLineItem.title:
                lineItems.append(thisLineItem.id)

        # print('line items existed {}'.format(counter))
        self.assertEqual(counter, 24)

        # ordersDelivered = Order.objects.filter(status='delivered')
        # print('-----------------------------')
        # for thisOrder in ordersDelivered.iterator():
        #     orderLineItems = LineItem.objects.filter(Order=thisOrder)
        #     for thisLineItem in orderLineItems.iterator():
        #         print('title: {} ; lineitemID: {}'.format(
        #             thisLineItem.title, thisLineItem.id))

        # for index, val in enumerate(lineItems):
        #     print('lineitem id: {}'.format(val))

        productReviews = ProductReview.objects.all()
        for index, thisReviews in enumerate(productReviews):
            self.assertEqual(thisReviews.comment,
                             'lineItem id is {}'.format(lineItems[index]))
