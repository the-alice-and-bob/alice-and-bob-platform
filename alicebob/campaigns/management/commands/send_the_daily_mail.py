from django.core.management.base import BaseCommand

from campaigns.engine import send_daily_email


class Command(BaseCommand):
    help = 'Send the daily email'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("[*] Sending the daily email..."))
        send_daily_email()
        self.stdout.write(self.style.SUCCESS("[*] Done!"))
