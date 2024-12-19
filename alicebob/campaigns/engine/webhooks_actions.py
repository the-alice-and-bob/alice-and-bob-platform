import logging

from datetime import datetime

from django.utils import timezone
from django.db.transaction import atomic

from academy.models import Student

from ..sdk import AcumbamailAPI
from ..scoring import EmailEventScore
from ..models import EmailEventType, EmailEvent, EmailCampaigns

logger = logging.getLogger("db")


def handle_action(campaign_id: int, email: str, timestamp, event_type: EmailEventType):
    """
    Procesa el evento de apertura. Guarda un evento de apertura
    y actualiza el scoring del estudiante si corresponde.
    """
    try:
        campaign = EmailCampaigns.objects.prefetch_related("mail_list").get(acumbamail_id=campaign_id)
    except EmailCampaigns.DoesNotExist:
        logger.warning(f"Email campaign '{campaign_id}' not found when processing event: {event_type} for email: {email}")
        return

    # Busca el estudiante relacionado con el email (si existe)
    try:
        student = Student.objects.get(email=email)
    except Student.DoesNotExist:
        logger.warning(f"Student not found for email when processing event: {event_type} for email: {email}")
        student = None

    # Registra el evento en el modelo EmailEvent
    with atomic():
        try:
            fixed_timestamp = timezone.make_aware(timestamp)
        except Exception:
            logger.warning(f"Invalid timestamp when processing event: {event_type} for email: {email}: {timestamp}")
            fixed_timestamp = timezone.now()

        EmailEvent.objects.create(
            campaign=campaign,
            student=student,
            email=email,
            event_type=EmailEventType.OPEN,
            timestamp=fixed_timestamp
        )

        campaign.increment_stat(event_type)

        # Actualiza el score del estudiante
        if student:

            if event_type == EmailEventType.OPEN:
                score_increment = EmailEventScore.OPEN
            elif event_type == EmailEventType.CLICK:
                score_increment = EmailEventScore.CLICK
            elif event_type == EmailEventType.COMPLAINT:
                score_increment = EmailEventScore.COMPLAINT
            elif event_type == EmailEventType.HARD_BOUNCE:
                score_increment = EmailEventScore.HARD_BOUNCE
            elif event_type == EmailEventType.SOFT_BOUNCE:
                score_increment = EmailEventScore.SOFT_BOUNCE
            elif event_type == EmailEventType.UNSUBSCRIBE:
                score_increment = EmailEventScore.UNSUBSCRIBE
            elif event_type == EmailEventType.DELIVERED:
                score_increment = EmailEventScore.DELIVERED
            else:
                score_increment = 0  # Para eventos no definidos

            student.email_engagement_score += score_increment
            student.update_score(auto_save=False)

            # Si el evento es una queja, de-suscripción o rebote duro, de-suscribir al estudiante
            if event_type in [EmailEventType.COMPLAINT, EmailEventType.UNSUBSCRIBE, EmailEventType.HARD_BOUNCE]:
                student.mail_lists.remove(campaign.mail_list)

                # Elimina al estudiante de la lista de leads
                AcumbamailAPI().delete_subscriber(
                    email=email,
                    list_id=campaign.mail_list.acumbamail_id
                )

            student.save()


__all__ = (
    'handle_action',
)
