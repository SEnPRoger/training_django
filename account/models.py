# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# class MyAccountManager(BaseUserManager):
#     def create_user(self, email, username, password=None):
#         if not email:
#             raise ValueError("Users must have an email")
#         if not username:
#             raise ValueError("Users must have an username")
        
#         user = self.model(
#             email = self.normalize_email(email),
#             username = username
#         )
#         user.set_password(password)
#         user.save(using=self._db)

#         return user
    
#     def create_superuser(self, email, username, password):
#         user = self.create_user(
#             username = username,
#             email = self.normalize_email(email),
#             password = password,
#         )

#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)

#         return user

# def username_photo_path(instance, filename):
#         # file will be uploaded to media/accounts/username/username.extension,
#         #                     like media/accounts/SEnPRoger/SEnPRoger.jpg
#         extension = filename.split('.')[1]
#         return 'accounts/{0}/{0}.{1}'.format(instance.username, extension)

# class Account(AbstractBaseUser):
#     username        = models.CharField(max_length=32, blank=False, unique=True)
#     photo           = models.ImageField(upload_to=username_photo_path, default='default.jpg', blank=False)
#     email           = models.EmailField(max_length=32, blank=False, unique=True)
#     password        = models.EmailField(max_length=32, blank=False, unique=True)

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     objects = MyAccountManager()

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

#Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email")
        if not username:
            raise ValueError("Users must have an username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            username = username,
            email = self.normalize_email(email),
            password = password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

def username_photo_path(instance, filename):
        # file will be uploaded to media/accounts/username/username.extension,
        #                     like media/accounts/SEnPRoger/SEnPRoger.jpg
        extension = filename.split('.')[1]
        return 'accounts/{0}/{0}.{1}'.format(instance.username, extension)

class Account(AbstractBaseUser):
    username        = models.CharField(max_length=32, blank=False, unique=True)
    photo           = models.ImageField(upload_to=username_photo_path, default='default.jpg', blank=False)
    email           = models.EmailField(max_length=32, blank=False, unique=True)
    password        = models.CharField(max_length=32, blank=False)
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def check_password(self, password):
        if password == self.password:
            return True
        else:
            return False
    
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)