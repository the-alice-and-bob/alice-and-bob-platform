from django.core.management.base import BaseCommand

from campaigns.sdk import update_list_from_acumbamail


class Command(BaseCommand):
    help = 'update acumbamail lists'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("[*] Syncing Acumbamail lists..."))
        update_list_from_acumbamail()
        self.stdout.write(self.style.SUCCESS("[*] Done!"))
