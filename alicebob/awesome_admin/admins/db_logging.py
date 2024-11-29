from django.contrib import admin

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
