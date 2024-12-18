from django.core.management.base import BaseCommand

from ezycourse.engine import populate_students


class Command(BaseCommand):
    help = 'Load all EzyCourse students in the database'
    name = 'populate_students'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Populating students to the database..."))

        for st in populate_students():
            self.stdout.write(self.style.SUCCESS(f"Student '{st.email} - {st.full_name}' populated successfully"))

