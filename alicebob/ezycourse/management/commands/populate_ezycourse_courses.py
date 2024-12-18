from django.core.management.base import BaseCommand

from ezycourse.engine import populate_courses


class Command(BaseCommand):
    help = 'Load all EzyCourses in the database'

    def handle(self, *args, **options):

        self.stdout.write("Populating courses to the database...")
        for c in populate_courses():
            self.stdout.write(f"Course {c} populated")
