from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from awesome_admin.mixing import SuperUserOnlyMixin
from zoho.models import ZohoOAuth, ZohoTag, ZohoLead, ZohoContact, ZohoPurchaseOrders, ZohoCourseProgress, ZohoProduct


# Register your models here.
@admin.register(ZohoOAuth)
class ZohoOAuthModelAdmin(SuperUserOnlyMixin, ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_display = ['api_domain', 'client_id']


@admin.register(ZohoTag)
class ZohoTagModelAdmin(SuperUserOnlyMixin, ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    def is_synced(self, obj):
        return obj.zoho_id is not None

    # Mostrar el nombre con el color del tag.
    def tag_color(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 6px; color: white; border-radius: 5px;">{}</span>',
            obj.tag.color_code, obj.tag.name
        )

    is_synced.boolean = True
    is_synced.short_description = 'Synced to Zoho'
    list_display = ['zoho_id', 'tag_color', 'is_synced']


@admin.register(ZohoLead)
class ZohoLeadModelAdmin(SuperUserOnlyMixin, ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    def student_name(self, obj):
        return obj.student.full_name

    def student_email(self, obj):
        return obj.student.email

    def is_synced(self, obj):
        return obj.zoho_id is not None

    is_synced.boolean = True
    is_synced.short_description = 'Synced to Zoho'
    list_display = ['zoho_id', 'student_name', 'student_email', 'is_synced']


@admin.register(ZohoContact)
class ZohoContactModelAdmin(SuperUserOnlyMixin, ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    def student_name(self, obj):
        return obj.student.full_name

    def student_email(self, obj):
        return obj.student.email

    def is_synced(self, obj):
        return obj.zoho_id is not None

    is_synced.boolean = True
    is_synced.short_description = 'Synced to Zoho'
    list_display = ['zoho_id', 'student_name', 'student_email', 'is_synced']


@admin.register(ZohoPurchaseOrders)
class ZohoPurchaseOrdersModelAdmin(SuperUserOnlyMixin, ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    def is_synced(self, obj):
        return obj.zoho_id is not None

    def sell_price(self, obj):
        return f'{obj.sell.sell_price}€'

    is_synced.boolean = True
    is_synced.short_description = 'Synced to Zoho'
    list_display = ['zoho_id', 'student', 'product', 'is_synced', 'sell_price']


@admin.register(ZohoCourseProgress)
class ZohoCourseProgressModelAdmin(SuperUserOnlyMixin, ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

    def is_synced(self, obj):
        return obj.zoho_id is not None

    def student_name(self, obj):
        return obj.student.full_name

    def student_email(self, obj):
        return obj.student.email

    def product_name(self, obj):
        return obj.product.product_name

    is_synced.boolean = True
    is_synced.short_description = 'Synced to Zoho'
    list_display = ['zoho_id', 'student_name', 'student_email', 'product_name', 'is_synced']
