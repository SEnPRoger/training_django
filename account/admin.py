from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_local_date_joined')
    search_fields = ('username', 'email')
    # readonly_fields = ('date_joined', 'last_login')
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    @admin.display(description='Joined date')
    def get_local_date_joined(self, obj):
        return obj.date_joined.strftime('%d %B %Y %H:%M')
    
    get_local_date_joined.admin_order_field = 'date_joined'
    # get_local_date_joined.short_description = 'Precise Time'

admin.site.register(Account, AccountAdmin)