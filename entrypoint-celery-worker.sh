#!/usr/bin/env sh

export C_FORCE_ROOT="true"

celery -A celery_app worker -l info --concurrency=3 --pool=prefork -B --scheduler django_celery_beat.schedulers:DatabaseScheduler
