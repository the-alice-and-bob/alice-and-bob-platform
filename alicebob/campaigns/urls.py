from django.urls import path
from .webhooks import *


urlpatterns = [
    path('', acumbamail_webhooks, name='acumbamail_webhooks'),
]
