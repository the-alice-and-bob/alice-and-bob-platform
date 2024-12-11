import os
from typing import List

from django.shortcuts import redirect
from django.urls import path, reverse_lazy, URLPattern
from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.text import slugify
from django.utils.html import format_html
from django.utils.translation import gettext as _
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from alicebob_sdk import TagListMixin
from campaigns.sdk import AcumbamailAPI, update_list_from_acumbamail

from .models import Product, Sells, Student, CourseProgress, Tag


# Register your models here.
@admin.register(Product)
class ProductAdmin(ModelAdmin, TagListMixin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    def display_price(self, obj):
        return f'{obj.price}€'

    display_price.short_description = 'Price'
    list_display = ['product_name', 'tag_list', 'ezy_id', 'display_price']
    list_filter = ['price', 'tags']

    def get_urls(self) -> List[URLPattern]:
        urls = super().get_urls()
        custom_urls = [
            path('create-acumbamail-lists/', self.create_acumbamail_lists, name='create-acumbamail-lists'),
        ]
        return custom_urls + urls

    def create_acumbamail_lists(self, request):
        # Get all products
        products = Product.objects.all()

        ac = AcumbamailAPI()

        # Create a list in Acumbamail for each product
        for product in products:
            # Código para crear listas en Acumbamail
            list_name = f"alicebob-{product.product_type.lower()}-{slugify(product.product_name)}"

            ac.create_mail_list(
                list_name,
                f'Lista de correo para compradores de {product.product_name}'
            )

        # Actualizar las listas desde Acumbamail
        update_list_from_acumbamail()

        # Código para crear listas en Acumbamail
        return redirect(reverse_lazy('admin:academy_product_changelist'))


@admin.register(Sells)
class SellsAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    search_fields = ['student__name', 'product__product_name', 'student__email']

    def display_price(self, obj):
        return f'{obj.sell_price}€'

    list_filter = ['date']
    list_display = ['student', 'product', 'date', 'display_price']


@admin.register(Student)
class StudentAdmin(ModelAdmin, TagListMixin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_filter = ['tags']
    list_display = ['email', 'name', 'tag_list', 'products_free', 'products_paid', 'see_sells']
    search_fields = ['email', 'name']

    def see_sells(self, obj):
        return format_html(
            '<a target="_blank" href="{}?student__id__exact={}">Ver compras &rarr;</a>',
            reverse_lazy('admin:academy_sells_changelist'),
            obj.id
        )

    see_sells.short_description = 'Compras'

    def products_free(self, obj):
        # Número de productos gratuitos que ha comprado el estudiante.
        return obj.sells.filter(product__price__lte=0).count()

    def products_paid(self, obj):
        # Número de productos de pago que ha comprado el estudiante.
        return obj.sells.filter(product__price__gt=0).count()

    products_free.short_description = _('Free products')
    products_paid.short_description = _('Paid products')

    # -------------------------------------------------------------------------
    # Custom actions
    # -------------------------------------------------------------------------
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'student-leads/',
                self.admin_site.admin_view(self.student_leads_view),
                name='admin-student-leads'
            ),
            path(
                'student-paid/',
                self.admin_site.admin_view(self.student_paid),
                name='admin-student-paid'
            ),
        ]
        return custom_urls + urls

    def student_leads_view(self, request):
        """
        Vista personalizada que reutiliza la plantilla de changelist y usa un queryset específico.
        """
        # Estudiantes que solo han comprado productos gratuitos y no de pago
        custom_queryset = Student.objects.filter(sells__product__price__lte=0).exclude(sells__product__price__gt=0).distinct()

        self.get_queryset = lambda r: custom_queryset
        return super().changelist_view(request)

    def student_paid(self, request):
        """
        Vista personalizada que reutiliza la plantilla de changelist y usa un queryset específico.
        """
        self.get_queryset = lambda r: Student.objects.filter(sells__product__price__gt=0).distinct()
        return super().changelist_view(request)


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
