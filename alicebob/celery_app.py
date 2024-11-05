import os

from pathlib import Path

from celery import Celery

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

# Discover all the subdirectories in the background_tasks directory
# and register them with Celery
modules = ["alicebob.background_tasks"]

here = Path(__file__).parent

for d in os.listdir(here / "background_tasks"):
    if os.path.isdir(here / "background_tasks" / d):
        modules.append(f"alicebob.background_tasks.{d}")

app_celery.autodiscover_tasks(modules)
