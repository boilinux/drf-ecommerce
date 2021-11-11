from django.db import models

# Create your models here.


class LineItem(models.Model):
    Account = models.ForeignKey('account.Account', related_name='line_item_user',
                                on_delete=models.CASCADE)
    Product = models.ForeignKey('product.Product', related_name='line_item_product',
                                on_delete=models.CASCADE)
    Order = models.ForeignKey('order.Order', related_name='line_item_order',
                              on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.CharField(max_length=100, blank=True)
    quantity = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'line item'
        verbose_name_plural = 'line items'

    def __str__(self):
        return self.title


class LineItemImage(models.Model):
    LineItem = models.ForeignKey('cart.LineItem', related_name='line_item_image',
                                 on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='files/product')

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    def __str__(self):
        return self.LineItem.title
