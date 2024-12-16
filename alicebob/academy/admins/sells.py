from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from ..models import Sells


@admin.register(Sells)
class SellsAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    search_fields = ['student__name', 'product__product_name', 'student__email']

    def display_price(self, obj):
        return f'{obj.sell_price}€'

    list_filter = ['date']
    list_display = ['student', 'product', 'date', 'display_price']

__all__ = ('SellsAdmin',)
