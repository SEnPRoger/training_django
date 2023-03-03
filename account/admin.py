from django.contrib import admin
from account.models import Account
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

    list_display = ('username', 'id', 'email', 'get_local_date_joined', 'is_moderator', 'is_admin')
    list_filter = ('is_moderator', 'is_admin', 'created_at',)
    fieldsets = (
        ('User credentials', {
            'fields': ('email', 'password')
        },),
        ('Personal info', {
            'fields': (('username', 'changed_username'), 'image_tag', 'photo', 'get_local_date_joined', 'city', 'country', 'is_moderator'),
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
    readonly_fields=('get_local_date_joined', 'image_tag', 'city', 'country', 'is_moderator')
    filter_horizontal = ()

admin.site.register(Account, AccountAdmin)

from django.contrib.auth.models import Group
admin.site.unregister(Group)