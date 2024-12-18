from django_celery_beat.models import PeriodicTask, IntervalSchedule

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'update acumbamail lists'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("[*] Creating periodic tasks. Execute ever 10 seconds"))

        schedule, _ = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)

        PeriodicTask.objects.create(
            interval=schedule,
            name='example_demo_task',
            task='example_demo_task',
        )
