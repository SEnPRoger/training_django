from django.db import models
from django.template.defaultfilters import truncatechars  # or truncatewords

# Create your models here.
class Comment(models.Model):
    author                      = models.ForeignKey('account.Account', related_name='author_set', on_delete=models.DO_NOTHING)
    content                     = models.CharField(max_length=516, blank=False)
    published_date              = models.DateTimeField(auto_now_add=True)
    is_edited                   = models.BooleanField(default=False)
    has_spoiler                 = models.BooleanField(default=False)
    device_type                 = models.CharField(max_length=16)
    replies                     = models.ManyToManyField("self", blank=True, related_name='replies_set', 
                                                         symmetrical=False)

    def __str__(self):
        return truncatechars(self.content, 100)
    
    @property
    def short_content(self):
        return truncatechars(self.content, 100)