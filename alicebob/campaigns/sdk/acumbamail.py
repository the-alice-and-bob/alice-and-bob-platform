import time
from dataclasses import dataclass

from datetime import datetime
from typing import Iterable

from django.conf import settings

import requests


@dataclass
class MailList:
    name: str
    identifier: int
    description: str
    subscribers: int = 0
    unsubscribed: int = 0
    bounced: int = 0


class AcumbamailAPI:

    def __init__(self, auth_token: str = None):
        self.auth_token = auth_token or settings.ACUMBAMAIL_TOKEN
        self.base_url = "https://acumbamail.com/api/1/"

    def _call_api(self, endpoint, data=None):
        if data is None:
            data = {}

        data['auth_token'] = self.auth_token
        data['response_type'] = 'json'
        url = self.base_url + endpoint + '/'

        while True:
            response = requests.post(url, json=data)

            if response.status_code == 429:
                print("Acumbamail API rate limit exceeded. Waiting 10 seconds.")
                time.sleep(10)
                continue

            break

        try:
            return response.json()
        except ValueError:
            return response.text

    def send_one(self, from_email, to_email, body, subject, category=''):
        data = {
            "from_email": from_email,
            "to_email": to_email,
            "body": body,
            "subject": subject,
            "category": category,
        }
        return self._call_api("sendOne", data)

    def send_many(
            self,
            campaign_name: str,
            subject: str,
            body: str,
            list_id: int = None,
            sender_name: str = None,
            sender_email: str = None,
            scheduled_date: datetime = None,
    ):
        sender_name = sender_name or settings.DEFAULT_SENDER_NAME
        sender_email = sender_email or settings.DEFAULT_SENDER_EMAIL
        list_id = list_id or settings.DEFAULT_LIST_ID

        html_content = f"""<body>
{body}
    <div style="margin-top: 40px; width: 100%; text-align: center; font-size: 60%; text-color: #dedede;">
        Aunque te echaremos de menos, si no quieres recibir más correos puedes <a style="text-color: #b1b1b1; font-size: 70%;" href="*|UNSUBSCRIBE_URL|*">darte de baja aquí.</a>
    </div>
</body>
        """

        data = {
            "name": campaign_name,
            "from_name": sender_name,
            "from_email": sender_email,
            "lists": [list_id],
            "content": html_content,
            "subject": subject,
            "complete_json": 1,
            "auth_token": self.auth_token,
            "response_type": "json",
        }

        if scheduled_date:
            # (Formato : YYYY-MM-DD HH:MM)
            data["date_send"] = scheduled_date.strftime("%Y-%m-%d %H:%M")

        return self._call_api("createCampaign", data)

    def add_subscriber(self, email: str, name: str, ezycourse_id: str, list_id: str = None):
        list_id = list_id or settings.DEFAULT_LIST_ID

        data = {
            "list_id": list_id,
            "merge_fields": {
                "email": email,
                "name": name,
                "ezycourse_id": ezycourse_id,
            }

        }
        return self._call_api("addSubscriber", data)

    # -------------------------------------------------------------------------
    # Mail List
    # -------------------------------------------------------------------------
    def create_mail_list(self, name, description):
        data = {
            "name": name,
            "sender_email": settings.DEFAULT_SENDER_EMAIL,
            "company": settings.DEFAULT_SENDER_COMPANY,
            "description": description,
            "country": settings.DEFAULT_SENDER_COUNTRY,
        }
        return self._call_api("createList", data)

    def get_mail_lists(self) -> Iterable[MailList]:
        for k, v in self._call_api("getLists").items():
            subscribers = self.get_list_stats(k)

            try:
                yield MailList(
                    name=v['name'],
                    identifier=k,
                    description=v['description'],
                    subscribers=subscribers['total_subscribers'],
                    unsubscribed=subscribers['unsubscribed_subscribers'],
                    bounced=subscribers['hard_bounced_subscribers'],
                )
            except KeyError:
                yield MailList(
                    name=v['name'],
                    identifier=k,
                    description=v['description'],
                )

    def get_list_subscribers(self, list_id):
        return self._call_api("getSubscribers", {"list_id": list_id})

    def get_list_stats(self, list_id):
        return self._call_api("getListStats", {"list_id": list_id})


__all__ = ("AcumbamailAPI",)