from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from product import views

app_name = 'product'

urlpatterns = format_suffix_patterns([
    path('product', views.ProductViews.as_view(),
         name="post_put_delete_product"),
    path('product/<int:pk>', views.ProductViews.as_view(),
         name="post_put_delete_product"),
    path('products/favorites', views.ProductFavoriteViews.as_view(),
         name="post_products_favorites"),
    path('product/<int:product_id>/image', views.ProductImagesViews.as_view(),
         name="post_product_image"),
    path('product/<int:product_id>/image/<int:image_id>', views.ProductImagesViews.as_view(),
         name="delete_product_image"),
])
