import os

from pathlib import Path

import decouple
import sentry_sdk

from celery import Celery, signals

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

if not REDIS_URL:
    raise ValueError("REDIS_URL is not defined")

# Configuración de Celery independiente de Flask
app_celery = Celery(
    'alicebob',
    broker=REDIS_URL,
    backend=REDIS_URL
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
