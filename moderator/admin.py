from django.contrib import admin
from moderator.models import Moderator
from django.utils import timezone

# Register your models here.
class ModeratorAdmin(admin.ModelAdmin):
    @admin.display(description='Assigned date')
    def get_local_date_joined(self, obj):
        return timezone.localtime(obj.joined_date).strftime('%d %B %Y %H:%M')
    get_local_date_joined.admin_order_field = 'joined_date'

    @admin.display(description='Username')
    def get_username(self, obj):
        return obj.account.username
    
    @admin.action(description='Delete moderators [WORKS]')
    def delete_moderator(modeladmin, request, queryset):
        for moderator in queryset:
            moderator.delete()

    list_display = ('get_username', 'id', 'get_local_date_joined',)
    list_filter = ('joined_date',)
    # fieldsets = (
    #     ('Personal info', {'fields': ('get_local_date_joined',)}),
    # )
    ordering = ('joined_date',)
    # readonly_fields=('get_local_date_joined',)
    actions = [delete_moderator]

admin.site.register(Moderator, ModeratorAdmin)