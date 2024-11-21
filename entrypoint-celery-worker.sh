#!/usr/bin/env sh

celery -A celery_app worker -l info --concurrency=4 --pool=gevent --uid=alicebob
