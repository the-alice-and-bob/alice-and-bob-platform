from datetime import datetime
from typing import List

from django.contrib import admin
from django.forms import ModelForm
from django.shortcuts import redirect
from django.urls import URLPattern, path, reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _

from import_export.admin import ImportExportModelAdmin

from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.decorators import display

from alicebob_sdk import celery_or_function
from awesome_admin.mixing import RRSSOnlyMixin
from .engine import create_send_campaign_email

from .sdk import sync_list_from_acumbamail
from .models import EmailCampaigns, MailList


class EmailCampaignsForm(ModelForm):
    class Meta:
        model = EmailCampaigns
        fields = ['subject', 'content', 'scheduled_at', 'mail_list']
        widgets = {
            'content': WysiwygWidget(attrs={'rows': 20, 'style': 'height: 500px; width: 100%;'}),
        }
        required_fields = ['subject', 'content', 'mail_list']


@admin.register(EmailCampaigns)
class EmailCampaignsAdmin(RRSSOnlyMixin, ModelAdmin, ImportExportModelAdmin):
    form = EmailCampaignsForm
    import_form_class = ImportForm
    export_form_class = ExportForm
    search_fields = ['subject', 'content']
    list_display = ['campaign_name', 'subject', 'mail_list', "is_sent"]
    fieldsets = (
        (
            _("Campaign Info"), {
                'fields': (
                    'subject',
                    'content',
                    'mail_list')
            }
        ),
        (
            _("Schedule"), {
                'fields': (
                    'scheduled_at',
                )
            }
        )
    )
    ordering = ['-created']

    @display(description="Campaign Name")
    def campaign_name(self, obj):
        if obj.scheduled_at:
            date = obj.scheduled_at.strftime("%Y-%m-%d")
        else:
            date = obj.created.strftime("%Y-%m-%d")

        return f"[{date}] {obj.subject}"

    def response_add(self, request, obj, post_url_continue=None):
        # If in the request is a parameter called "_send_now", send the email now and redirect to the change view, without
        # saving the object

        if '_send_now' in request.POST:

            # User message
            self.message_user(request, _("El email se ha enviado correctamente"))

            # Send the email
            obj.is_sent = True
            obj.send_date = datetime.now()
            obj.schedule_at = None
            obj.save()

            celery_or_function(create_send_campaign_email, 'task_create_send_campaign_email', obj.pk)

            # Redirect to the change view
            change_url = reverse('admin:campaigns_emailcampaigns_changelist')
            return redirect(change_url)

        else:
            return super().response_add(request, obj, post_url_continue)


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
        sync_list_from_acumbamail()

        self.message_user(request, "Listas de correo actualizadas correctamente")

        # redirección a la raiz del modelo en el admin
        app, model = self.get_model_info()
        return redirect(reverse(f'admin:{app}_{model}_changelist'))

    def acumbamail_id(self, obj):
        return format_html(f'<a href="https://acumbamail.com/app/list/{obj.acumbamail_id}/" target="_blank">{obj.acumbamail_id}</a>')
