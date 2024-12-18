from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'update acumbamail lists'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("[*] Creating interval schedules. Execute every 10 seconds"))

        # Create a new interval schedule: 10, 30, 1h, 2h, 8h, 10h, 12h, 24h
        schedules = (
            (10, IntervalSchedule.SECONDS),
            (30, IntervalSchedule.SECONDS),
            (1, IntervalSchedule.MINUTES),
            (2, IntervalSchedule.MINUTES),
            (8, IntervalSchedule.HOURS),
            (10, IntervalSchedule.HOURS),
            (12, IntervalSchedule.HOURS),
            (24, IntervalSchedule.HOURS),
        )

        for every, period in schedules:
            schedule, _ = IntervalSchedule.objects.get_or_create(every=every, period=period)

        self.stdout.write(self.style.SUCCESS("[*] Creating cron schedules. Execute every day at 9:30, 12:30, 15:30, 18:30, 21:30"))
        # Create cron schedules: every day at 9:30, 12:30, 15:30, 18:30, 21:30. As base time is Europe/Madrid, not UTC for timezone
        cron_schedules = (
            ('30 9 * * *',),
            ('30 12 * * *',),
            ('30 15 * * *',),
            ('30 18 * * *',),
            ('30 21 * * *',),
        )

        for cron in cron_schedules:
            minute, hour, day_of_week, day_of_month, month_of_year = cron[0].split()
            CrontabSchedule.objects.get_or_create(
                minute=minute, hour=hour, day_of_week=day_of_week, day_of_month=day_of_month, month_of_year=month_of_year,
                timezone='Europe/Madrid'
            )
