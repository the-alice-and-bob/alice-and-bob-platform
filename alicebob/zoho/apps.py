from django.apps import AppConfig


class ZohoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'zoho'

    def ready(self):
        import zoho.signals
