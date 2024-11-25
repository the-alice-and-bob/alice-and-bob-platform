import json
from typing import List, Iterable, Dict
from dataclasses import dataclass, field

import requests

from awesome_ezycourse.sdk.auth import Auth


class FormError(Exception):
    ...


@dataclass
class Form:
    auth: Auth
    identifier: int
    name: str
    count_responses: int

    @classmethod
    def from_json(cls, auth, data: dict):
        return cls(
            auth=auth,
            identifier=data["id"],
            name=data["form_name"],
            count_responses=data["response_count"]
        )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Form {self.identifier} - {self.name} ({self.count_responses} responses)>"

    def get_schema(self) -> List[str]:
        url_schema = "/api/form_builder/get-form-builder-all/"
        url = f"{self.auth.site}{url_schema}{self.identifier}"

        """
        Response JSON format:
        
        {
          "id": 1911,
          "form_name": "Navaja Negra - optin-3F78DA70-7546-447A-B8A3-7376777106BF",
          "form_schema": "[{\"name\":\"Nombre\",\"type\":\"text\",\"required\":false,\"max\":50,\"min\":3,\"key\":\"Nombre\",\"placeholder\":\"Nombre\"},{\"name\":\"Email\",\"type\":\"email\",\"required\":true,\"key\":\"email\",\"placeholder\":\"Email\"}]",
          "email_me": 1,
          "third_party_service": "",
          "third_party_service_list_id": "",
          "school_id": 794,
          "created_at": "2024-10-17T09:41:46.000+00:00",
          "updated_at": "2024-10-23T14:41:38.000+00:00",
          "double_opt_in": 0,
          "webhook_url": "",
          "webhook_enabled": 0
        }
        """
        response = requests.get(
            url,
            headers=self.auth.get_headers()
        )

        if response.status_code != 200:
            raise Exception(f"Failed to fetch form schema: {response.text}")

        data = response.json()

        try:
            schema = json.loads(data["form_schema"])
        except json.JSONDecodeError:
            raise FormError("Failed to parse form schema")

        return [
            item["key"] for item in schema
        ]

    def get_responses(self) -> Iterable[Dict[str, str]]:
        """
        Get all responses for this form
        """

        """URL format:
        /api/form_builder/get-form-response-v2/1911?lesson_id=undefined&page=all&sort=asc
        """

        query_params = {
            "lesson_id": "undefined",
            "page": "all",
            "sort": "asc"
        }

        url = f"{self.auth.site}/api/form_builder/get-form-response-v2/{self.identifier}"

        response = requests.get(
            url,
            headers=self.auth.get_headers(),
            params=query_params
        )

        if response.status_code != 200:
            raise Exception(f"Failed to fetch responses: {response.text}")

        data = response.json()

        return data


class Forms:
    URL_LIST_FORMS = "/api/form_builder/get-form-types"

    def __init__(self, auth: "Auth"):
        self.auth = auth

    def get(self, identifier: int) -> Form:
        """
        Get a form by its identifier
        """

        forms = self.list_forms()

        for form in forms:
            if form.identifier == identifier:
                return form

        raise FormError(f"Form {identifier} not found in the platform")

    def list_forms(self) -> List[Form]:
        """
        Get all forms from the platform
        """

        """
        Response JSON format:

        [
          {
            "form_name": "Navaja Negra - optin-3F78DA70-7546-447A-B8A3-7376777106BF",
            "id": 1911,
            "double_opt_in": 0,
            "response_count": 20
          }
        ]
        """
        target_url = f"{self.auth.site}{self.URL_LIST_FORMS}"

        response = requests.get(
            target_url,
            headers=self.auth.get_headers()
        )

        if response.status_code != 200:
            raise Exception(f"Failed to fetch forms: {response.text}")

        data = response.json()

        return [Form.from_json(self.auth, item) for item in data]


__all__ = ("Form", "Forms", "FormError")
