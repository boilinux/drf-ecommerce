from django.db import models

# Create your models here.


class Store(models.Model):
    Account = models.ForeignKey('account.Account', related_name='store_user',
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
    image = models.ImageField(upload_to='files/store')
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'store'
        verbose_name_plural = 'store'

    def __str__(self):
        return self.name


class StoreImage(models.Model):
    Store = models.ForeignKey('store.Store', related_name='store_image',
                              on_delete=models.CASCADE)
    image = models.ImageField(upload_to='files/store')

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    def __str__(self):
        return self.Store.name
