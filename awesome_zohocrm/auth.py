import abc
import time
import json

from pathlib import Path

import requests


class AuthException(Exception):
    ...


class AuthenticationStorage(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_auth_data(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def save_auth_data(
            self,
            client_id: str,
            client_secret: str,
            refresh_token: str,
            grant_token: str,
            expires_in: int,
            access_token: str
    ):
        raise NotImplementedError


class FileAuthenticationStorage(AuthenticationStorage):

    def __init__(self, path: str = None):
        self._path = path or Path.home() / ".alicebob" / "zoho_auth.json"

    def get_auth_data(self) -> dict:
        try:
            with open(self._path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise AuthException("Auth data file not found")

        return data

    def save_auth_data(
            self,
            client_id: str,
            client_secret: str,
            refresh_token: str,
            grant_token: str,
            expires_in: int,
            access_token: str
    ):
        # save to file
        with open(self._path, "w") as token_file:
            json.dump({
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "grant_token": grant_token,
                "expires_in": expires_in,
                "access_token": access_token
            }, token_file)


class Auth:

    def __init__(self, auth_storage: AuthenticationStorage = None, api_domain: str = "https://www.zohoapis.eu"):
        self._storage = auth_storage or FileAuthenticationStorage()

        self._client_id = None
        self._client_secret = None
        self._refresh_token = None
        self._grant_token = None
        self._expires_in = None
        self._access_token = None

        self.api_domain = api_domain

    @property
    def http_headers(self) -> dict:
        return {
            "Authorization": f"Zoho-oauthtoken {self.access_token}",
        }

    @property
    def access_token(self) -> str:
        if not self._access_token:
            data = self._storage.get_auth_data()

            try:
                self._client_id = data["client_id"]
                self._client_secret = data["client_secret"]
                self._refresh_token = data["refresh_token"]
                self._grant_token = data["grant_token"]
                self._expires_in = data["expires_in"]
                self._access_token = data["access_token"]
            except KeyError:
                raise AuthException("Invalid data in data")

            # Check expiry time and that will not expire in the next 5 minutes
            if self._expires_in < time.time() + 300:
                self._refresh_access_token()

        return self._access_token

    def _refresh_access_token(self):
        """
        Refresh the access token and save it to the file
        """

        """
        Json data example:

        {
            "access_token": "1000.a36bfd630098e860880d6b04abf1e496.f576dec9254e5ce210102ea6600753ee",
            "scope": "ZohoCRM.modules.ALL ZohoCRM.users.ALL ZohoCRM.settings.ALL",
            "api_domain": "https://www.zohoapis.eu",
            "token_type": "Bearer",
            "expires_in": 3600
        }
        """
        data = {
            "refresh_token": self._refresh_token,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "grant_type": "refresh_token"
        }

        response = requests.post("https://accounts.zoho.eu/oauth/v2/token", data=data)

        if response.status_code != 200:
            raise AuthException("Error refreshing token")

        data = response.json()

        self._access_token = data["access_token"]
        self._expires_in = time.time() + data["expires_in"]

        self._storage.save_auth_data(
            client_id=self._client_id,
            client_secret=self._client_secret,
            refresh_token=self._refresh_token,
            grant_token=self._grant_token,
            expires_in=self._expires_in,
            access_token=self._access_token
        )

    def ping(self) -> bool:
        """
        Simulate a ping to the Zoho API
        :return:
        """
        ping_url = f"{self.api_domain}/crm/v2/modules"

        response = requests.get(ping_url, headers=self.http_headers)

        if "INVALID_TOKEN" in response.text:
            self._refresh_access_token()

            response = requests.get(ping_url, headers=self.http_headers)

            if "INVALID_TOKEN" in response.text:
                return False

            return True

        else:
            return True
