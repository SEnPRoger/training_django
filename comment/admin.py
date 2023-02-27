from django.contrib import admin
from django.utils import timezone
from comment.models import Comment
from account.models import Account
from django.db import models
from .forms import CommentForm

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    form = CommentForm

    @admin.display(description='Published date')
    def get_published_date(self, obj):
        return timezone.localtime(obj.published_date).strftime('%d %B %Y %H:%M')
    get_published_date.admin_order_field = 'published_date'

    @admin.display(description='Comment author')
    def get_author_username(self, obj):
        return obj.author.username
    
    @admin.display(description='Replies amount')
    def get_replies_amount(self, obj):
        return obj.replies.count()

    list_display = ('short_content', 'id', 'get_author_username', 'get_published_date', 'get_replies_amount', 'is_edited', 'has_spoiler', 'device_type')
    list_filter = ('published_date', 'device_type', 'has_spoiler',)
    ordering = ('published_date',)
    readonly_fields=('get_published_date',)

admin.site.register(Comment, CommentAdmin)