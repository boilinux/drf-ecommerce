from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from store import views

app_name = 'store'

urlpatterns = format_suffix_patterns([
    path('store/create', views.StoreCreateViews.as_view(), name="create_store"),
    path('store/update', views.StoreUpdateViews.as_view(), name="update_store"),
    path('store/disable/<int:pk>',
         views.StoreDisableViews.as_view(), name="disable_store"),
    path('store/image',
         views.StoreImageViews.as_view(), name="create_image"),
])
