"""
This file defines the Acumbamail webhooks for handling different events.
"""
import logging

from django.conf import settings
from django.http import JsonResponse
from django.utils.timezone import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from celery_app import app as background
from alicebob_sdk.decorators import *

from .models import EmailEventType
from .engine.webhooks_actions import handle_action

logger = logging.getLogger(__name__)


# Helper function to convert UNIX timestamp to readable datetime
def convert_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


ACUMBAMAIL_EVENTS = {
    'subscribes': EmailEventType.SUBSCRIBE,
    'unsubscribes': EmailEventType.UNSUBSCRIBE,
    'delivered': EmailEventType.DELIVERED,
    'hard_bounces': EmailEventType.HARD_BOUNCE,
    'soft_bounces': EmailEventType.SOFT_BOUNCE,
    'complaints': EmailEventType.COMPLAINT,
    'opens': EmailEventType.OPEN,
    'clicks': EmailEventType
}


@csrf_exempt
@require_http_methods(['POST'])
@authorize
@ensure_json
def acumbamail_webhooks(request):
    """
    Processes webhooks from Acumbamail for a given list_id.
    """
    events = request.json  # Assuming input is already in JSON format.

    # Ensure the events structure is valid and is a list
    if not isinstance(events, dict):
        return JsonResponse({'error': 'Invalid JSON payload, expected a list of events.'}, status=400)

    # Iterate through all events in the payload
    """
    Payload Example:
    {
        "1":
        {
            "email_key": "f64f8ed342c8ae988bfba6f74f210b90",
            "timestamp": 1734439351.0,
            "campaign_id": 2990070,
            "email": "daniel@abirtone.com",
            "list_id": 1035387,
            "subscriber_fields":
            {
                "email": "daniel@abirtone.com",
                "name": "Daniel"
            },
            "event": "opens"
        },
        "2":
        {
            "email_key": "f64f8ed342c8ae988bfba6f74f210b90",
            "timestamp": 1734439351.0,
            "campaign_id": 2990070,
            "email": "daniel@abirtone.com",
            "list_id": 1035387,
            "subscriber_fields":
            {
                "email": "daniel@abirtone.com",
                "name": "Daniel"
            },
            "event": "opens"
        }
    }
    
    """
    for event in events.values():
        event_type = event.get('event')
        email = event.get('email')
        timestamp = event.get('timestamp')
        campaign_id = event.get('campaign_id')

        if not event_type or not email or not timestamp or not campaign_id:
            logger.warning(f"Invalid event data: {event}")
            continue

        try:
            event_type = ACUMBAMAIL_EVENTS[event_type]
        except KeyError:
            logger.warning(f"Unhandled event type: {event_type} for email: {email}")
            continue

        if settings.DEBUG:
            logger.debug(f"Processing event: {event_type} for email: {email} at {timestamp}")
            handle_action(campaign_id, email, timestamp, event_type)
        else:
            background.send_task('task_process_acumbamail_webhook', args=(campaign_id, email, timestamp, event_type))

    return JsonResponse({'message': 'Webhook processed successfully'})

__all__ = (
    'acumbamail_webhooks',
)
