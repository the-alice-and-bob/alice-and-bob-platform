from django.contrib import admin
from unfold.admin import ModelAdmin

from zoho.models import ZohoOAuth


# Register your models here.
@admin.register(ZohoOAuth)
class ZohoOAuthModelAdmin(ModelAdmin):
    pass
