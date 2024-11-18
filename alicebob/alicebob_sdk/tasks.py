from django.conf import settings
from celery_app import app


def celery_or_function(func, *args, **kwargs):
    """
    This function will call directly the function or will call the celery "send_task" function if the Django configuration
    is set to use Celery.
    """
    call_celery = getattr(settings, 'USE_CELERY', False)

    if call_celery:
        return app.send_task(func, args=args, kwargs=kwargs)

    return func(*args, **kwargs)


__all__ = ('celery_or_function', )
