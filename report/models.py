from django.db import models
from django.template.defaultfilters import truncatechars  # or truncatewords

# Create your models here.
class Report(models.Model):
    report_from_account         = models.ForeignKey('account.Account', related_name='report_from_set', on_delete=models.DO_NOTHING)
    report_date                 = models.DateTimeField(auto_now_add=True)
    report_comment              = models.ForeignKey('comment.Comment', related_name='report_comment', on_delete=models.DO_NOTHING)

    def __str__(self):
        return truncatechars(self.report_comment.content, 100)