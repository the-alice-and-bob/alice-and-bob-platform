from django.contrib import admin
from django.forms import ModelForm
from django.utils.html import format_html
from django.db import models

from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from .models import News, NewsTag, NewsChannel, NewsProvider


class NewsAdminForm(ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'content': WysiwygWidget(),
            'telegram_text': WysiwygWidget(),
        }


@admin.register(News)
class NewsAdmin(ModelAdmin, ImportExportModelAdmin):
    # override the default form field for the content field, but only the field "content"
    form = NewsAdminForm
    import_form_class = ImportForm
    export_form_class = ExportForm

    def tag_list(self, obj):
        return format_html(' '.join([
            format_html(
                '<span style="background-color: {}; padding: 6px; color: white; border-radius: 5px;">{}</span>',
                tag.color, tag.name
            )
            for tag in obj.tags.all()
        ]))

    tag_list.short_description = 'Tags'
    search_fields = ['title', 'content']
    list_display = ['title', 'state', 'origin', 'published', 'tag_list']
    list_filter = ['state', 'origin', 'tags']

#
# @admin.register(NewsTag)
# class NewsTagAdmin(ModelAdmin, ImportExportModelAdmin):
#     import_form_class = ImportForm
#     export_form_class = ExportForm
#
#     def tag_color(self, obj):
#         return format_html(
#             '<span style="background-color: {}; padding: 6px; color: white; border-radius: 5px;">{}</span>',
#             obj.color, obj.name
#         )
#
#     tag_color.short_description = 'Tag'
#     list_display = ['tag_color']
#
#
# @admin.register(NewsChannel)
# class NewsChannelAdmin(ModelAdmin, ImportExportModelAdmin):
#     import_form_class = ImportForm
#     export_form_class = ExportForm
#
#     list_display = ['name', 'provider']
#     list_filter = ['provider']
#
#
# @admin.register(NewsProvider)
# class NewsProviderAdmin(ModelAdmin, ImportExportModelAdmin):
#     import_form_class = ImportForm
#     export_form_class = ExportForm
#
#     list_display = ['name']
