from django.contrib import admin
from django.utils import timezone
from report.models import Report

# Register your models here.
class ReportAdmin(admin.ModelAdmin):
    @admin.display(description='Report date')
    def get_report_date(self, obj):
        return timezone.localtime(obj.report_date).strftime('%d %B %Y %H:%M')
    get_report_date.admin_order_field = 'report_date'

    @admin.display(description='Report from account')
    def get_report_from_account_username(self, obj):
        return obj.report_from_account.username
    
    @admin.display(description='Report to account')
    def get_report_to_account_username(self, obj):
        return obj.report_comment.author

    list_display = ('report_comment', 'get_report_to_account_username', 'get_report_from_account_username', 'id', 'get_report_date')
    list_filter = ('report_date',)
    ordering = ('report_date',)
    readonly_fields=('get_report_date',)

admin.site.register(Report, ReportAdmin)