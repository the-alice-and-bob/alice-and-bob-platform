from django.conf import settings

from celery_app import app


def celery_or_function(func, celery_task_name: str, *args, **kwargs):
    """
    This function will call directly the function or will call the celery "send_task" function if the Django configuration
    is set to use Celery.
    """
    if settings.DEBUG:
        func(*args, **kwargs)

    else:
        app.send_task(celery_task_name, args=args, kwargs=kwargs)


__all__ = ('celery_or_function', )
