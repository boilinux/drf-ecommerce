from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from account import views

app_name = 'account'

urlpatterns = format_suffix_patterns([
    path('account/register', views.AccountRegisterViews.as_view(), name="register"),
    path('account/login', views.AccountLoginViews.as_view(), name="login"),
    path('account/logout', views.AccountLogoutViews.as_view(), name="logout"),
    path('account/update/password',
         views.AccountUpdatePasswordViews.as_view(), name="update_password"),
])
