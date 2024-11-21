FROM python:3.12-alpine AS base

RUN addgroup -S alicebob && \
    adduser -S -G alicebob -s /bin/false alicebob && \
    apk update && apk upgrade && apk add --no-cache curl

FROM base AS development

# Disable virtualenv creation
ENV POETRY_VIRTUALENVS_CREATE=false

#RUN apk add build-base libffi-dev openssl-dev && \
#    pip install --disable-pip-version-check --no-cache-dir -U pip poetry

RUN pip install --disable-pip-version-check --no-cache-dir -U pip poetry

COPY ./pyproject.toml pyproject.toml
COPY ./poetry.lock poetry.lock
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir --no-deps -r requirements.txt

COPY ./deployment/gunicorn.conf.py /gunicorn.conf.py
COPY ./entrypoint-web.sh /entrypoint-web
COPY ./entrypoint-celery-worker.sh /entrypoint-celery-worker
RUN chmod +x /entrypoint*

COPY ./alicebob /alicebob
COPY ./awesome_zohocrm /alicebob/awesome_zohocrm
COPY ./ezycourse /alicebob/ezycourse
RUN chown -R alicebob:alicebob /alicebob /awesome_zohocrm /ezycourse

WORKDIR /alicebob
ENTRYPOINT ["/entrypoint-web"]
