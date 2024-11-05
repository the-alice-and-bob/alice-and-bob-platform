#!/usr/bin/env sh

celery -A alicebob.celery_app worker -l info --concurrency=2 --pool=gevent --uid=alicebob
