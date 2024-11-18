import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from celery_app import app as app_celery


@csrf_exempt
def webhook_news(request):
    token = request.GET.get('token', None)

    if token != settings.URL_TOKEN:
        return JsonResponse({"error": "Invalid token"}, status=401)

    if not request.content_type == 'application/json':
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    data = json.loads(request.body)

    # app_celery.send_task('inoreader_distributor', args=(data,))

    return JsonResponse({"message": "Success"})
