import time

from typing import Iterable
from datetime import datetime
from dataclasses import dataclass

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

    def _ret_id(self, data: dict | str | int) -> int:
        try:
            return int(data)
        except (ValueError, TypeError):
            # Not an integer. Is it a dict?
            if type(data) is dict:
                return data['id']

            raise ValueError(f"Invalid data type: {type(data)}")

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

            # response code is not a 2xx
            if not response.ok:
                print(f"Acumbamail API error: {response.text}. Response code: {response.status_code}")

            break

        try:
            return response.json()
        except ValueError:
            return response.text

    def send_one(self, from_email, to_email, body, subject, category='') -> int:
        data = {
            "from_email": from_email,
            "to_email": to_email,
            "body": body,
            "subject": subject,
            "category": category,
        }
        self._ret_id(
            self._call_api("sendOne", data)
        )

    def send_many(
            self,
            campaign_name: str,
            subject: str,
            body: str,
            list_id: int,
            sender_name: str = None,
            sender_email: str = None,
            scheduled_date: datetime | None = None,
    ) -> int:
        sender_name = sender_name or settings.ACUMBAMAIL_SENDER_NAME
        sender_email = sender_email or settings.ACUMBAMAIL_SENDER_EMAIL

        html_content = f"""<body>
{body}
    <div style="margin-top: 40px; width: 100%; text-align: center; font-size: 60%; text-color: #dedede;">
        <p>Aunque te echaremos de menos, si no quieres recibir más correos puedes <a style="text-color: #b1b1b1; font-size: 70%;" href="*|UNSUBSCRIBE_URL|*">darte de baja aquí.</a></p>
        <p>Si te das de baja, no recibirás los emails, las novedades y las ofertas de que doy de vez en cuando. </p>
        <p>Además, no podrás leer el email en ningún otro sitio. Email que no recibas, email que te pierdes.</p>
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
            "tracking_urls": 1,
            "complete_json": 1,
            "response_type": "json",
        }

        if scheduled_date:
            # (Formato : YYYY-MM-DD HH:MM)
            data["date_send"] = scheduled_date.strftime("%Y-%m-%d %H:%M")

        return self._ret_id(
            self._call_api("createCampaign", data)
        )

    def add_subscriber(self, email: str, name: str, list_id: str | int):

        data = {
            "list_id": list_id,
            "merge_fields": {
                "email": email,
                "name": name
            }

        }
        return self._call_api("addSubscriber", data)

    def delete_subscriber(self, email: str, list_id: str | int):
        data = {
            "list_id": list_id,
            "email": email
        }
        return self._call_api("deleteSubscriber", data)

    # -------------------------------------------------------------------------
    # Mail List
    # -------------------------------------------------------------------------
    def create_mail_list(self, name, description):
        data = {
            "name": name,
            "sender_email": settings.ACUMBAMAIL_SENDER_EMAIL,
            "company": settings.ACUMBAMAIL_SENDER_COMPANY,
            "description": description,
            "country": settings.ACUMBAMAIL_SENDER_COUNTRY,
        }
        return self._ret_id(
            self._call_api("createList", data)
        )

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

            time.sleep(1)

    def get_list_subscribers(self, list_id):
        return self._call_api("getSubscribers", {"list_id": list_id})

    def get_list_stats(self, list_id):
        return self._call_api("getListStats", {"list_id": list_id})


__all__ = ("AcumbamailAPI",)
