from django.contrib import admin

from .models import Store, StoreImage


class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'Account', 'address', 'id')
    search_fields = ('name',)


class StoreImageAdmin(admin.ModelAdmin):
    list_display = ('Store', 'image')
    search_fields = ('Store',)


# Register your models here.
admin.site.register(Store, StoreAdmin)
admin.site.register(StoreImage, StoreImageAdmin)
