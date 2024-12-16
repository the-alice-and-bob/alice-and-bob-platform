from django.contrib import admin
from django.db import models
from django.shortcuts import render
from django.urls import reverse_lazy, path
from django.utils.html import format_html
from django.utils.translation import gettext as _
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.decorators import display

from alicebob_sdk import TagListMixin

from ..models import Student, Tag


# -------------------------------------------------------------------------
# All Students
# -------------------------------------------------------------------------
@admin.register(Student)
class StudentAdmin(ModelAdmin, TagListMixin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    tag_model = Tag

    list_filter = ['tags']
    list_display = ['email', 'name', 'tag_list', 'products_free', 'products_paid', 'see_sells']
    search_fields = ['email', 'name']

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display_links = None
        self.default_queryset = self.get_queryset

    @display(description=_('Sells'))
    def see_sells(self, obj):
        return format_html(
            '<a target="_blank" href="{}?student__id__exact={}">Ver compras &rarr;</a>',
            reverse_lazy('admin:academy_sells_changelist'),
            obj.id
        )

    @display(description=_('Free products'))
    def products_free(self, obj):
        # Número de productos gratuitos que ha comprado el estudiante.
        # return obj.sells.filter(product__price__lte=0).count()
        return obj.products_free

    @display(description=_('Paid products'))
    def products_paid(self, obj):
        # Número de productos de pago que ha comprado el estudiante.
        # return obj.sells.filter(product__price__gt=0).count()
        return obj.products_paid

    def get_queryset(self, request):
        query = super().get_queryset(request)

        query = self.tags_queryset(query)

        # Prefetch the sells and anotate the count of free and paid products per student.
        return query.prefetch_related('sells', 'tags').annotate(
            products_free=models.Count('sells', filter=models.Q(sells__sell_price__lte=0), distinct=True),
            products_paid=models.Count('sells', filter=models.Q(sells__sell_price__gt=0), distinct=True),
        )

    # -------------------------------------------------------------------------
    # Custom actions
    # -------------------------------------------------------------------------
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'students-all/',
                self.students_all,
                name='admin-student-all'
            ),
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

    def students_all(self, request):
        self.get_queryset = self.default_queryset
        return super().changelist_view(request)

    def student_leads_view(self, request):
        """
        Vista personalizada que reutiliza la plantilla de changelist y usa un queryset específico.
        """
        # Estudiantes que solo no han pagado por productos. Es decir, que el precio de venta es 0.
        query = self.default_queryset(request)

        query = query.prefetch_related('sells__product').filter(sells__sell_price__lte=0).exclude(sells__sell_price__gt=0).only(
            "email", "name"
        ).distinct()

        self.get_queryset = lambda r: query.all()

        return self.changelist_view(request)

    def student_paid(self, request):
        """
        Vista personalizada que reutiliza la plantilla de changelist y usa un queryset específico.
        """
        query = self.default_queryset(request)

        query = query.prefetch_related('sells__product').filter(sells__sell_price__gt=0).only("email", "name").distinct()

        self.get_queryset = lambda r: query.all()

        return super().changelist_view(request)


# -------------------------------------------------------------------------
# Leads
# -------------------------------------------------------------------------
# @admin.register(StudentLeadProxy)
# class StudentLeadAdmin(ModelAdmin, StudentAdminBase, TagListMixin, ImportExportModelAdmin):
#     import_form_class = ImportForm
#     export_form_class = ExportForm
#     tag_model = Tag
#
#     list_filter = ['tags']
#     list_display = ['email', 'name', 'tag_list', 'products_free', 'products_paid', 'see_sells']
#     search_fields = ['email', 'name']
#
#     def get_queryset(self, request):
#         query = super().get_queryset(request)
#         return query.prefetch_related('sells__product').filter(
#             sells__product__price__lte=0
#         ).exclude(sells__product__price__gt=0).only("email", "name").distinct()
#
#
# # -------------------------------------------------------------------------
# # Contacts
# # -------------------------------------------------------------------------
# @admin.register(StudentContactProxy)
# class StudentPaidAdmin(ModelAdmin, StudentAdminBase, TagListMixin, ImportExportModelAdmin):
#     import_form_class = ImportForm
#     export_form_class = ExportForm
#     tag_model = Tag
#
#     list_filter = ['tags']
#     list_display = ['email', 'name', 'tag_list', 'products_free', 'products_paid', 'see_sells']
#     search_fields = ['email', 'name']
#
#     def get_queryset(self, request):
#         query = super().get_queryset(request)
#         return query.prefetch_related('sells__product').filter(
#             sells__product__price__gt=0
#         ).only("email", "name").distinct()
