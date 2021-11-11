from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'Account', 'full_name', 'phone_number', 'notes', 'delivery_fee', 'status')
    search_fields = ('id', 'Account__id', 'notes', 'delivery_fee', 'status')
# Register your models here.


admin.site.register(Order, OrderAdmin)
