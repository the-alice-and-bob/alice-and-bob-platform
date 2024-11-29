from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from ezycourse.models import EzyCourseAuth
from awesome_admin.mixing import SuperUserOnlyMixin


@admin.register(EzyCourseAuth)
class EzyCourseAuthModelAdmin(SuperUserOnlyMixin, ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_display = ['email', 'site']
