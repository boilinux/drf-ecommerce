from django.db import models

# Create your models here.


class Order(models.Model):
    Account = models.ForeignKey('account.Account', related_name='user_order',
                                on_delete=models.CASCADE)
    total = models.CharField(max_length=100)
    datetime = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    address = models.TextField(max_length=500)
    notes = models.TextField(max_length=500, blank=True)
    delivery_fee = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return self.phone_number
