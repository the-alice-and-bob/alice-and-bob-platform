from typing import List

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import URLPattern, path, reverse_lazy
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.decorators import display

from alicebob_sdk import TagListMixin
from campaigns.sdk import AcumbamailAPI, update_list_from_acumbamail

from ..models import Product, Tag


# Register your models here.
@admin.register(Product)
class ProductAdmin(ModelAdmin, TagListMixin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    tag_field_name = Tag

    @display(description='Price')
    def display_price(self, obj):
        return f'{obj.price}€'

    list_display = ['product_name', 'tag_list', 'ezy_id', 'display_price']
    list_filter = ['price', 'tags']

    def get_queryset(self, request):
        query = super().get_queryset(request)

        query = self.tags_queryset(query)

        return query.all()

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

            ac.create_mail_list(
                product.slug_name,
                f'Lista de correo para compradores de {product.product_name}'
            )

        # Actualizar las listas desde Acumbamail
        update_list_from_acumbamail()

        # Código para crear listas en Acumbamail
        return redirect(reverse_lazy('admin:academy_product_changelist'))


__all__ = ('ProductAdmin',)
