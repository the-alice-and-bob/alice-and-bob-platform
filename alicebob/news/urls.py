from django.urls import path

from .views import webhook_news

urlpatterns = [
    path('news', webhook_news, name='news-webhook'),
]
