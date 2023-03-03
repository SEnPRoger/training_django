from account.views import *
from django.urls import path, include

app_name = "account"

urlpatterns = [
    
    path('register/', AccountRegister.as_view(), name='register'),
    path('login/', AccountLogin.as_view(), name='login'),

    path('detail/', AccountProfile.as_view(), name='detail'),
    path('upload_photo/', AccountPhotoUpload.as_view(), name='upload_photo'),
    path('get/<str:username>/', AccountGetAnother.as_view(), name='get_account'),
]