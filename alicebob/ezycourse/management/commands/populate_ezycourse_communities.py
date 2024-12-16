from django.core.management.base import BaseCommand

from ezycourse.sdk import populate_communities


class Command(BaseCommand):
    help = 'Load all EzyCourses communities to the database'

    def handle(self, *args, **options):

        self.stdout.write("Populating EzyCourses communities...")
        for c in populate_communities():
            self.stdout.write(f"Community {c.product_name} created")
