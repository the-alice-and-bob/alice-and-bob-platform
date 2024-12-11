from django.contrib import admin
from django.utils.html import format_html

from unfold.admin import ModelAdmin
from django_db_logger.models import StatusLog
from django_db_logger.admin import StatusLogAdmin

from awesome_admin.mixing import SuperUserOnlyMixin

admin.site.unregister(StatusLog)


# Personaliza la clase administrativa para Group
# class CustomGroupAdmin(GroupAdmin, ModelAdmin, SuperUserOnlyMixin):
@admin.register(StatusLog)
class CustomStatusLogAdmin(SuperUserOnlyMixin, StatusLogAdmin, ModelAdmin):
    """
    Admin para el modelo Group con restricciones de permisos.
    """

    search_fields = ['msg']
    list_display = ["create_datetime", "colored_msg", "custom_trace"]

    def custom_message(self, obj):
        return obj.msg[:50]

    def custom_trace(self, instance):
        return format_html('<pre><code>{content}</code></pre>', content=instance.trace if instance.trace else '')

    # custom_message.short_description = 'Mensaje'
