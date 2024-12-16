from django.contrib import admin
from django.forms import ModelForm, URLInput, Textarea
from django.utils.html import format_html
from django.db import models

from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget, ArrayWidget
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from awesome_admin.mixing import TagListMixin

from .models import News, NewsTag, NewsChannel, NewsProvider


class NewsAdminForm(ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'content': WysiwygWidget(attrs={'rows': 20, 'style': 'height: 300px; width: 100%;'}),
            'telegram_text': WysiwygWidget(attrs={'rows': 20, 'style': 'height: 300px; width: 100%;'}),
            'tag_list': ArrayWidget(),
        }
        # change the labels of the fields
        labels = {
            'content': 'Contenido original',
            'telegram_text': 'Texto para Telegram',
            'linkedin_text': 'Texto para LinkedIn',
            'twitter_text': 'Texto para Twitter',
            'ezy_text': 'EzyCourse text',
        }


@admin.register(News)
class NewsAdmin(ModelAdmin, TagListMixin, ImportExportModelAdmin):
    # override the default form field for the content field, but only the field "content"
    form = NewsAdminForm
    import_form_class = ImportForm
    export_form_class = ExportForm

    search_fields = ['title', 'content']
    list_display = ['title', 'state', 'origin', 'published', 'tag_list']
    list_filter = ['state', 'origin', 'tags']
    fields = [
        'title', 'url', 'image', 'content', 'linkedin_text', 'telegram_text', 'twitter_text', 'ezy_text', 'tags', 'origin', 'scheduled'
    ]


@admin.register(NewsTag)
class NewsTagAdmin(ModelAdmin, TagListMixin, ImportExportModelAdmin):
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
