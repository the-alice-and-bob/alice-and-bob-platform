from campaigns.models import MailList

from .acumbamail import AcumbamailAPI


def sync_list_from_acumbamail():
    ac = AcumbamailAPI()

    existing_mail_ids = set()

    # Get all mail lists from Acumbamail and keep their IDs
    for _list in ac.get_mail_lists():
        print(f"Syncing list {_list.name}")

        try:
            mail_list = MailList.objects.get(acumbamail_id=_list.identifier)
            mail_list.subscribers = _list.subscribers
            mail_list.unsubscribed = _list.unsubscribed
            mail_list.bounced = _list.bounced
            mail_list.save()
        except MailList.DoesNotExist:
            print(f"La lista {_list.name} no existe en la base de datos, se creará desde Acumbamail")

            MailList.objects.create(
                name=_list.name,
                acumbamail_id=_list.identifier,
                description=_list.description,
                subscribers=_list.subscribers,
                unsubscribed=_list.unsubscribed,
                bounced=_list.bounced,
            )

        existing_mail_ids.add(_list.identifier)

    # Disable or remove mail lists that are not in Acumbamail

    # Those lists that were not using, then delete it

    # Those lists that were using, then disable it
    MailList.objects.exclude(acumbamail_id__in=existing_mail_ids).update(active=False)


__all__ = ('sync_list_from_acumbamail',)
