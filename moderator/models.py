from django.db import models
from account.models import Account

# Create your models here.
class Moderator(models.Model):
    account = models.ForeignKey('account.Account', related_name='account_set', on_delete=models.DO_NOTHING)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account.username
    
    def save(self, *args, **kwargs):
        super(Moderator, self).save(*args, **kwargs)
        self.account.moderator_id = self.id
        self.account.is_moderator = True
        self.account.save()
        super(Moderator, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.account.moderator_id = None
        self.account.is_moderator = False
        self.account.save()
        super().delete()