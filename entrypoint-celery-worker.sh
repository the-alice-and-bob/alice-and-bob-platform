#!/usr/bin/env sh

celery -A celery_app worker -l info --concurrency=3 --pool=prefork -B --scheduler django_celery_beat.schedulers:DatabaseScheduler
