#!/usr/bin/env sh

export GUNICORN_LOG_LEVEL="${LOG_LEVEL:-INFO}"

exec gunicorn --log-level "${GUNICORN_LOG_LEVEL}" -c /gunicorn.conf.py  --bind ":8080" -w 5 -k gevent --timeout 0 --backlog 512 --worker-connections 512 alicebob.web:app