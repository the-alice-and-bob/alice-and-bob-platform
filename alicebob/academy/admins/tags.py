from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from ..models import Tag


@admin.register(Tag)
class TagAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    # Mostrar el nombre con el color del tag.
    def tag_color(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 6px; color: white; border-radius: 5px;">{}</span>',
            obj.color_code, obj.name
        )

    tag_color.short_description = 'Tag'
    list_display = ['tag_color']


__all__ = ('TagAdmin',)
