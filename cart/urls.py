from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from cart import views

app_name = 'cart'

urlpatterns = format_suffix_patterns([
    path('cart', views.CartViews.as_view(),
         name="post_delete_cart"),
    path('cart/<int:pk>', views.CartViews.as_view(),
         name="post_delete_cart"),
])
