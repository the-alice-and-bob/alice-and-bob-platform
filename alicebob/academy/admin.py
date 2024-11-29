from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from .models import Product, Sells, Student, CourseProgress, Tag


# Register your models here.
@admin.register(Product)
class ProductAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    def display_price(self, obj):
        return f'{obj.price}€'

    def tag_list(self, obj):
        return format_html(' '.join([
            format_html(
                '<span style="background-color: {}; padding: 6px; color: white; border-radius: 5px;">{}</span>',
                tag.color_code, tag.name
            )
            for tag in obj.tags.all()
        ]))

    tag_list.short_description = 'Tags'
    display_price.short_description = 'Price'
    list_display = ['product_name', 'tag_list', 'ezy_id', 'display_price']
    list_filter = ['price', 'tags']


@admin.register(Sells)
class SellsAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    def display_price(self, obj):
        return f'{obj.sell_price}€'

    list_filter = ['date']
    list_display = ['student', 'product', 'date', 'display_price']


@admin.register(Student)
class StudentAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    def tag_list(self, obj):
        return format_html(' '.join([
            format_html(
                '<span style="background-color: {}; padding: 6px; color: white; border-radius: 5px;">{}</span>',
                tag.color_code, tag.name
            )
            for tag in obj.tags.all()
        ]))

    list_filter = ['tags']
    list_display = ['email', 'name', 'ezy_id', 'tag_list']


@admin.register(CourseProgress)
class CourseProgressAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_filter = ['progress']
    ordering = ['progress']
    list_display = ['progress', 'student', 'course']


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

