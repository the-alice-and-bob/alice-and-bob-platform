FROM python:3.12-alpine

RUN addgroup -S alicebob && \
    adduser -S -G alicebob -s /bin/false alicebob && \
    apk update && apk upgrade && apk add --no-cache curl && \
    mkdir /staticfiles /data

ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install --disable-pip-version-check --no-cache-dir -U pip poetry poetry-plugin-export

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
COPY ./awesome_ezycourse /alicebob/awesome_ezycourse
RUN chown -R alicebob:alicebob /alicebob /staticfiles /data

WORKDIR /alicebob
RUN python manage.py collectstatic --noinput
ENTRYPOINT ["/entrypoint-web"]
