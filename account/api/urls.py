from account.api.views import *
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

app_name = "account"

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('settings', UserView.as_view(), name='settings'),
    path('logout', LogoutView.as_view(), name='logout')
    # path('logout', logout_view, name='logout'),
    # # path('accounts/', include("django.contrib.auth.urls")),
    # path('username-available', username_available_view, name='username_available'),
    # path('email-available', email_available_view, name='email_available'),
]