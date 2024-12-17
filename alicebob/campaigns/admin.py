from typing import List

from django.contrib import admin
from django.forms import ModelForm
from django.shortcuts import redirect
from django.urls import URLPattern, path, resolve, reverse
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin

from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from awesome_admin.mixing import RRSSOnlyMixin

from .sdk import update_list_from_acumbamail
from .models import EmailCampaigns, MailList


class DailyEmailAdminForm(ModelForm):
    class Meta:
        model = EmailCampaigns
        fields = ['subject', 'content', 'scheduled_at', 'mail_list']
        widgets = {
            'content': WysiwygWidget(attrs={'rows': 20, 'style': 'height: 500px; width: 100%;'}),
        }


@admin.register(EmailCampaigns)
class DailyEmailAdmin(RRSSOnlyMixin, ModelAdmin, ImportExportModelAdmin):
    form = DailyEmailAdminForm
    import_form_class = ImportForm
    export_form_class = ExportForm
    fields = ['subject', 'content', 'scheduled_at', 'mail_list']
    search_fields = ['subject', 'content']
    list_display = ['campaign_name', 'subject', 'mail_list']

    def campaign_name(self, obj):
        if obj.scheduled_at:
            date = obj.scheduled_at.strftime("%Y-%m-%d")
        else:
            date = obj.created.strftime("%Y-%m-%d")

        return f"[{date}] {obj.subject}"

    campaign_name.short_description = 'Campaign Name'


@admin.register(MailList)
class MailListAdmin(RRSSOnlyMixin, ModelAdmin, ImportExportModelAdmin):
    fields = ['name', 'description', 'subscribers', 'unsubscribed', 'bounced', 'acumbamail_id']
    search_fields = ['name', 'description']
    list_display = ['name', 'subscribers', 'unsubscribed', 'bounced', "active_bullet"]
    list_filter = ['name']
    list_per_page = 10
    list_max_show_all = 100
    ordering = ['-subscribers']

    def active_bullet(self, obj):
        return True if obj.active else False

    active_bullet.short_description = 'Active'
    active_bullet.boolean = True
#
#     def action_button(self, obj):
#         # Format in tailwindcss
#         return format_html("""
# <div class="block w-full">
#     <ul class="border flex flex-col font-medium rounded shadow-sm bg-white dark:bg-gray-900 md:flex-row">
#         <li class="border-b flex-grow text-center md:border-b-0 md:border-r last:border-0">
#             <a href="/ee4ea7f6-804f-49fd-a357-941b92b64159/campaigns/maillist/import/" class="block p-2 text-sm font-medium text-gray-700
#             dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800">
#                 Import
#             </a>
#         </li>
#         <li class="border-b flex-grow text-center md:border-b-0 md:border-r last:border-0">
#             <a href="/ee4ea7f6-804f-49fd-a357-941b92b64159/campaigns/maillist/export/?" class="block p-2 text-sm font-medium
#             text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800">
#                 Exports
#             </a>
#         </li>
#     </ul>
# </div>
# """)
#
#     action_button.short_description = 'Action'

    def get_urls(self) -> List[URLPattern]:
        urls = super().get_urls()

        # add custom urls here
        custom_urls = [
            path('reload-mail-list/', self.admin_site.admin_view(self.reload_mail_list), name='reload-mail-list'),
        ]

        return custom_urls + urls

    def reload_mail_list(self, request):
        # Reload the mail list
        update_list_from_acumbamail()

        self.message_user(request, "Listas de correo actualizadas correctamente")

        # redirección a la raiz del modelo en el admin
        app, model = self.get_model_info()
        return redirect(reverse(f'admin:{app}_{model}_changelist'))

    def acumbamail_id(self, obj):
        return format_html(f'<a href="https://acumbamail.com/app/list/{obj.acumbamail_id}/" target="_blank">{obj.acumbamail_id}</a>')
