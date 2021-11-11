from django.contrib import admin

from .models import Favorites, Product, ProductImage

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',
                    'price', 'stock', 'free_shipping', 'id')
    search_fields = ('title', 'description')


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('Account', 'Product', 'isfavorite')
    search_fields = ('Account__username', 'Product__title',
                     'Product__description')


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('Product', 'image')
    search_fields = ('Product__title',
                     'Product__description')


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
