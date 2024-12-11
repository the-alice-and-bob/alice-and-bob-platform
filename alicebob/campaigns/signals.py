from datetime import datetime

from django.dispatch import receiver
from django.db.models.signals import post_save

from campaigns.models import DailyEmail

from .sdk import AcumbamailAPI


@receiver(post_save, sender=DailyEmail)
def send_email(sender, instance, created, **kwargs):
    if created:
        acu = AcumbamailAPI()
        acu.send_many(
            campaign_name=f"[{datetime.today().strftime('%Y-%m-%d')}] {instance.subject}",
            subject=instance.subject,
            body=instance.content,
            scheduled_date=instance.scheduled_at,
            list_id=instance.mail_list.acumbamail_id,
        )
