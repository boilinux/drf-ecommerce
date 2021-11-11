from django.db import models

# Create your models here.


class Product(models.Model):
    Store = models.ForeignKey('store.Store', related_name='store_owner_product',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to='files/product')
    stock = models.BooleanField(default=True)
    free_shipping = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title


class Favorites(models.Model):
    Account = models.ForeignKey('account.Account', related_name='account_product_favorites',
                                on_delete=models.CASCADE)
    Product = models.ForeignKey('product.Product', related_name='product_favorites',
                                on_delete=models.CASCADE)
    isfavorite = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'favorite'
        verbose_name_plural = 'favorites'

    def __str__(self):
        name = ""
        if self.Account is not None:
            name = self.Account.full_name
        else:
            name = "null_name"

        if self.Product is not None:
            name += " " + self.Product.title
        else:
            name += " null_product"

        return name


class ProductImage(models.Model):
    Product = models.ForeignKey('product.Product', related_name='product_images',
                                on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='files/product')

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    def __str__(self):
        return self.Product.title


class ProductReview(models.Model):
    Product = models.ForeignKey('product.Product', related_name='product_review',
                                on_delete=models.CASCADE)
    Account = models.ForeignKey('account.Account', related_name='user_product_review',
                                on_delete=models.CASCADE)
    Order = models.ForeignKey('order.Order', related_name='user_order',
                              on_delete=models.CASCADE)
    rating = models.CharField(max_length=50)
    comment = models.TextField(max_length=500)
    datetime = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'

    def __str__(self):
        return self.datetime
