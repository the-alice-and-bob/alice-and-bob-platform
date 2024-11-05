#!/usr/bin/env sh

celery -A alicebob.celery_app worker -l info --concurrency=10 --pool=gevent --uid=alicebob
