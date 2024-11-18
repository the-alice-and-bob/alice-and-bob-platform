from django.conf import settings
from django.http import HttpResponseForbidden


def authorize(view_func):
    """
    This decorator checks if a view function is authorized to be accessed.

    To do that, it check a query parameter called 'token' that should be passed. This parameter is mandatory and configured via settings.
    """
    def wrapper(request, *args, **kwargs):
        token = request.GET.get('token')
        if token != settings.AUTH_TOKEN:
            return HttpResponseForbidden()

        return view_func(request, *args, **kwargs)

    return wrapper


__all__ = ('authorize', )
