import os
import ssl

from pathlib import Path

import decouple
import sentry_sdk

from celery import Celery, signals

# CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672//')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND_URL', None)

if not CELERY_BROKER_URL:
    raise ValueError("CELERY_BROKER_URL is not defined")

config = {
    'CELERY_BROKER_URL': CELERY_BROKER_URL,
}

if CELERY_BACKEND:
    config['result_backend'] = CELERY_BACKEND

if CELERY_BROKER_URL.startswith('rediss') or CELERY_BACKEND.startswith('rediss'):
    config['broker_use_ssl'] = {
        'ssl_cert_reqs': ssl.CERT_NONE
    }
    config['redis_backend_use_ssl'] = {
        'ssl_cert_reqs': ssl.CERT_NONE
    }


# Configuración de Celery independiente de Flask
app_celery = Celery(
    'alicebob',
    **config
)

app_celery.conf.update(
    broker_connection_retry_on_startup=True,
)


# Initialize Sentry SDK on Celery startup
@signals.celeryd_init.connect
def init_sentry(**_kwargs):
    sentry_sdk.init(
        dsn=decouple.config('SENTRY_DSN'),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )


# Discover all the subdirectories in the background_tasks directory
# and register them with Celery
modules = ["alicebob.background_tasks"]

here = Path(__file__).parent

for d in os.listdir(here / "background_tasks"):
    if os.path.isdir(here / "background_tasks" / d):
        modules.append(f"alicebob.background_tasks.{d}")

app_celery.autodiscover_tasks(modules)
