from django.contrib import admin
from account.models import Account
from moderator.models import Moderator
from comment.models import Comment
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class AccountAdmin(BaseUserAdmin):

    @admin.display(description='Joined date')
    def get_local_date_joined(self, obj):
        return timezone.localtime(obj.created_at).strftime('%d %B %Y %H:%M')
    get_local_date_joined.admin_order_field = 'created_at'

    @admin.display(description='Changed username')
    def get_local_date_changed(self, obj):
        return obj.changed_username.strftime('%d %B %Y %H:%M')
    
    @admin.display(description='Assigned date')
    def get_moderator_assigned_date(self, obj):
        return timezone.localtime(Moderator.objects.get(id=obj.moderator_id).joined_date).strftime('%d %B %Y %H:%M')
    
    @admin.display(description='Comments amount')
    def get_comments_amount(self, obj):
        return Comment.objects.filter(author=obj.id).count()
    
    @admin.action(description='Create moderators from selected accounts')
    def create_moderator(modeladmin, request, queryset):
        for account in queryset:
            new_moderator = Moderator(account=account)
            new_moderator.save()

    @admin.action(description='Delete moderators from selected accounts')
    def delete_moderator(modeladmin, request, queryset):
        for account in queryset:
            moderator = Moderator.objects.get(account=account)
            if moderator is not None:
                moderator.delete()

    list_display = ('username', 'id', 'email', 'get_local_date_joined', 'get_comments_amount', 'is_moderator', 'is_admin')
    list_filter = ('is_moderator', 'is_admin', 'created_at',)
    fieldsets = (
        ('User credentials', {
            'fields': ('email', 'password')
        },),
        ('Personal info', {
            'fields': (('username', 'changed_username'), 'image_tag', 'photo', 'get_local_date_joined', 'city', 'country',),
        }),
        ('Group', {
            'fields':(('is_moderator', 'moderator_id', 'get_moderator_assigned_date'),),
        }),
        ('Permissions', {
            'fields': ('is_admin',),
            'classes': ('collapse',),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'photo', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username',)
    ordering = ('created_at',)
    readonly_fields=('get_local_date_joined', 'image_tag', 'city', 'country', 'is_moderator', 'moderator_id', 'get_moderator_assigned_date')
    filter_horizontal = ()
    actions = [create_moderator, delete_moderator]

admin.site.register(Account, AccountAdmin)

from django.contrib.auth.models import Group
admin.site.unregister(Group)