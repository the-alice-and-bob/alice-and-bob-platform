import orjson
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseBadRequest


def authorize(view_func):
    """
    This decorator checks if a view function is authorized to be accessed.

    To do that, it check a query parameter called 'token' that should be passed. This parameter is mandatory and configured via settings.
    """
    def wrapper(request, *args, **kwargs):
        token = request.GET.get('token')

        if token != settings.URL_TOKEN:
            return HttpResponseForbidden()

        return view_func(request, *args, **kwargs)

    return wrapper


def ensure_json(view_func):
    """
    This decorator ensures that the request has a JSON content type.
    """

    def wrapper(request, *args, **kwargs):
        if request.content_type != 'application/json':
            return HttpResponseBadRequest("Content type must be application/json")

        try:
            request.json = orjson.loads(request.body)
        except orjson.JSONDecodeError as e:
            return HttpResponseBadRequest("Invalid JSON")

        return view_func(request, *args, **kwargs)

    return wrapper


__all__ = ('authorize', 'ensure_json')
