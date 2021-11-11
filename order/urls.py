from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from order import views

app_name = 'order'

urlpatterns = format_suffix_patterns([
    path('order', views.OrderViews.as_view(),
         name="post_order"),
])
