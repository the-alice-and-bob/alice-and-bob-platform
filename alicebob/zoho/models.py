from django.db import models
from simple_history.models import HistoricalRecords


class ZohoOAuth(models.Model):
    client_id = models.CharField(max_length=255, unique=True)
    client_secret = models.CharField(max_length=255, unique=True)
    grant_token = models.CharField(max_length=255, unique=True)
    refresh_token = models.CharField(max_length=255, unique=True)
    access_token = models.CharField(max_length=255, unique=True)
    expiry_time = models.BigIntegerField()
    api_domain = models.CharField(max_length=255)
    redirect_uri = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"Client ID: {self.client_id} - {self.api_domain}"

    class Meta:
        verbose_name = "Zoho OAuth"
        verbose_name_plural = "Zoho OAuth"
        db_table = "zoho_oauth"
        # composed indexes
        indexes = [
            models.Index(fields=['access_token', 'refresh_token']),
        ]
