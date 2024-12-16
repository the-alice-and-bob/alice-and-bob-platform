from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from ..models import CourseProgress


@admin.register(CourseProgress)
class CourseProgressAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_filter = ['progress']
    ordering = ['progress']
    list_display = ['progress', 'student', 'course']

__all__ = ('CourseProgressAdmin',)
