from account.api.views import *
from django.urls import path, include

app_name = "account"

urlpatterns = [
    
    path('register/', AccountRegister.as_view(), name='register'),
    path('login/', AccountLogin.as_view(), name='login'),

    path('detail/', AccountProfile.as_view(), name='detail'),
    path('upload_photo/', AccountPhotoUpload.as_view(), name='upload_photo'),

    path('change_username/', AccountChangeUsername.as_view(), name='change_username'),
    path('change_password/', AccountChangePassword.as_view(), name='change_password'),

    path('logout/', AccountLogout.as_view(), name='logout'),
    path('delete/', AccountDelete.as_view(), name='delete'),

    path('available_username/', AccountCheckUsernameAvailable.as_view(), name='available_username'),
    path('available_email/', AccountCheckEmailAvailable.as_view(), name='available_email'),

    # path('reset_password_send_email/', AccountSendEmailResetPassword.as_view(), name='reset_password_send_email'),
    # path('reset_password/<uid>/<token>', AccountResetPassword.as_view(), name='reset_password_email'),
]