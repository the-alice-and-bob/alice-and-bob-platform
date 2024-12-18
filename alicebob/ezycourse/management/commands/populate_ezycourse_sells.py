from django.core.management.base import BaseCommand

from ezycourse.engine import populate_sells


class Command(BaseCommand):
    help = 'Load all EzyCourse students in the database'
    name = 'populate_students'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Populating students to the database..."))

        for st, pd in populate_sells():
            self.stdout.write(self.style.SUCCESS(f"Student '{st.email} - {st.full_name}' populated for course '{pd.product_name}'"))

