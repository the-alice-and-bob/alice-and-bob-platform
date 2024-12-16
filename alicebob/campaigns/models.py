from django.db import models

from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from academy.models import Student


class MailList(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    acumbamail_id = models.IntegerField(unique=True)

    subscribers = models.IntegerField(default=0)
    unsubscribed = models.IntegerField(default=0)
    bounced = models.IntegerField(default=0)

    users = models.ManyToManyField(Student, related_name="mail_lists", blank=True)

    active = models.BooleanField(default=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} ({self.subscribers})"

    class Meta:
        verbose_name = "Mail List"
        verbose_name_plural = "Mail Lists"
        db_table = "mail_list"


class DailyEmail(TimeStampedModel, models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()
    scheduled_at = models.DateTimeField(null=True, blank=True)

    mail_list = models.ForeignKey(MailList, on_delete=models.CASCADE, null=True, blank=True, related_name="daily_emails")

    def __str__(self):
        return f"{self.subject} - {self.created}"

    class Meta:
        verbose_name = "Daily Email"
        verbose_name_plural = "Daily Emails"
        db_table = "daily_emails"
