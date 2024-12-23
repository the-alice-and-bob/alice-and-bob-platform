from enum import Enum

from django.db import models

from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from academy.models import Student


class EmailEventType(Enum):
    OPEN = "open"
    CLICK = "click"
    COMPLAINT = "complaint"
    HARD_BOUNCE = "hard_bounce"
    SOFT_BOUNCE = "soft_bounce"
    DELIVERED = "delivered"
    UNSUBSCRIBE = "unsubscribe"
    SUBSCRIBE = "subscribe"


class MailList(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    acumbamail_id = models.IntegerField(unique=True)

    subscribers = models.IntegerField(default=0)
    unsubscribed = models.IntegerField(default=0)
    bounced = models.IntegerField(default=0)

    users = models.ManyToManyField(Student, related_name="mail_lists", blank=True)
    leads = models.ManyToManyField("academy.Lead", related_name="mail_lists", blank=True)

    active = models.BooleanField(default=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} ({self.subscribers})"

    class Meta:
        verbose_name = "Mail List"
        verbose_name_plural = "Mail Lists"
        db_table = "mail_list"


class EmailCampaigns(TimeStampedModel, models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()

    is_sent = models.BooleanField(default=False, help_text="Indica si el email ha sido enviado.", db_index=True)
    is_draft = models.BooleanField(default=True, help_text="Indica si el email es un borrador.", db_index=True)

    send_date = models.DateTimeField(null=True, blank=True, help_text="Fecha en la que se ha enviado el email.")
    scheduled_at = models.DateField(
        null=True, blank=True, db_index=True, help_text="Fecha en la que se programó el envío del email."
    )

    # día preferido para enviar el email: Lunes, Martes, Miércoles, Jueves, Viernes, Sábado, Domingo
    preferred_day = models.CharField(
        max_length=10,
        choices=[
            ("any", "Cualquier día"),
            ("monday", "Lunes"),
            ("tuesday", "Martes"),
            ("wednesday", "Miércoles"),
            ("thursday", "Jueves"),
            ("friday", "Viernes"),
            ("saturday", "Sábado"),
            ("sunday", "Domingo"),
        ],
        default="any",
        help_text="Día preferido para enviar el email."
    )

    acumbamail_id = models.IntegerField(unique=True, null=True, blank=True, db_index=True)
    mail_list = models.ForeignKey(MailList, on_delete=models.CASCADE, null=True, blank=True, related_name="daily_emails")

    # -------------------------------------------------------------------------
    # Stats
    # -------------------------------------------------------------------------
    total_sent = models.IntegerField(default=0, help_text="Total de emails enviados en esta campaña.")
    total_opens = models.IntegerField(default=0, help_text="Total de emails abiertos en esta campaña.")
    total_clicks = models.IntegerField(default=0, help_text="Total de clics registrados en esta campaña.")
    total_bounces = models.IntegerField(default=0, help_text="Total de rebotes registrados en esta campaña.")
    total_complaints = models.IntegerField(default=0, help_text="Total de quejas registradas en esta campaña.")
    total_unsubscribes = models.IntegerField(default=0, help_text="Total de de-suscripciones registradas en esta campaña.")

    def __str__(self):
        return f"{self.subject} - {self.created}"

    class Meta:
        verbose_name = "Email Campaign"
        verbose_name_plural = "Email Campaigns"
        db_table = "email_campaign"

    def increment_stat(self, event_type: EmailEventType, auto_save=True):
        """
        Incrementa el conteo de la estadística respectiva basado en el tipo de evento.
        """
        if event_type == EmailEventType.OPEN:
            self.total_opens += 1
        elif event_type == EmailEventType.CLICK:
            self.total_clicks += 1
        elif event_type in [EmailEventType.HARD_BOUNCE, EmailEventType.SOFT_BOUNCE]:
            self.total_bounces += 1
        elif event_type == EmailEventType.COMPLAINT:
            self.total_complaints += 1
        elif event_type == EmailEventType.UNSUBSCRIBE:
            self.total_unsubscribes += 1

        if auto_save:
            self.save()


class EmailEvent(TimeStampedModel, models.Model):
    """
    Representa un evento relacionado con un email enviado.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="email_events",
        null=True,
        blank=True,
        help_text="Estudiante relacionado al evento (si corresponde)."
    )
    email = models.EmailField(max_length=800, help_text="Email asociado al evento.")
    campaign = models.ForeignKey(
        EmailCampaigns,
        on_delete=models.CASCADE,
        related_name="email_events",
        null=True,
        blank=True,
        help_text="Email que disparó este evento."
    )
    event_type = models.CharField(
        max_length=50,
        choices=[
            (tag.value, tag.name)
            for tag in EmailEventType
        ],
        help_text="Tipo de evento registrado para este email."
    )
    timestamp = models.DateTimeField(help_text="Fecha y hora del evento.")
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Información adicional sobre el evento en formato JSON."
    )

    class Meta:
        verbose_name = "Email Event"
        verbose_name_plural = "Email Events"
        db_table = "email_event"

    def __str__(self):
        return f"{self.email} - {self.get_event_type_display()} ({self.timestamp})"
