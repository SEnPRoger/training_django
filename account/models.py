from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import shutil
from pathlib import Path

class AccountManager(BaseUserManager):
    def create_user(self, username, email, password=None, password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

def username_photo_path(instance, filename):
        # file will be uploaded to media/accounts/account.id/username.extension,
        #                     like media/accounts/1/SEnPRoger.jpg
        extension = filename.split('.')[1]
        return 'accounts/{0}/{1}.{2}'.format(instance.id, instance.username, extension)

# Create your models here.
class Account(AbstractBaseUser):
    username            = models.CharField(verbose_name='Username', max_length=32, blank=False, unique=True, help_text='Username should be unique')
    email               = models.EmailField(verbose_name='Email', max_length=32, blank=False, unique=True, help_text='Email should be unique')
    photo               = models.ImageField(verbose_name='Change account photo', upload_to=username_photo_path, blank=True)
    city                = models.CharField(max_length=64, blank=False)
    country             = models.CharField(max_length=64, blank=False)
    changed_username    = models.DateTimeField(verbose_name='Changed username date', default=datetime.datetime.now, help_text='Username can be changed every 24 hours')

    moderator_id        = models.IntegerField(blank=True, null=True)
    is_moderator        = models.BooleanField(default=False)

    is_active           = models.BooleanField(default=True)
    is_admin            = models.BooleanField(default=False)

    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def image_tag(self):
        from django.utils.html import mark_safe
        return mark_safe('<img src="%s" width="150" height="150" />' % (self.photo.url))
    image_tag.short_description = 'Account photo'
    image_tag.allow_tags = True

    def get_image(self):
        if self.photo:
            return self.photo.url

    def delete(self, using=None, keep_parents=False):
        try:
            if self.photo != None:
                photo_path = Path(self.photo.path)
                photo_folder = photo_path.parent
                shutil.rmtree(photo_folder)
        except:
            pass