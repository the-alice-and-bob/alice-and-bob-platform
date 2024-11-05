import json
import pathlib
from typing import Dict

from urllib.parse import unquote, urljoin

import requests

from .utils import check_site


class AuthError(Exception):
    ...


class Auth:
    """
    This class manages the authentication configuration for the SDK.
    """
    LOGIN_URL = "/api/student/auth/login"

    def __init__(self):
        """
        This method initializes the SDK.
        """
        self.__user_data: Dict[str, str or None] = {
            "site": None,
            "session_cookie": None,
            "access_token": None,
        }

        restored_data = self.__restore_user_data__()

        if restored_data:
            self.__user_data.update(restored_data)

    @property
    def site(self) -> str:
        """
        This method returns the site for the SDK.
        """
        try:
            s = self.__user_data["site"]

            if not s:
                raise AuthError("Site is not set")

            return s
        except KeyError:
            raise AuthError("Site is not set")

    @property
    def session_cookie(self) -> str:
        """
        This method returns the session cookie for the SDK.
        """
        try:
            s = self.__user_data["session_cookie"]

            if not s:
                raise AuthError("Session cookie is not set")

            return s
        except KeyError:
            raise AuthError("Session cookie is not set")

    def do_login(self, site: str, email: str, password: str):
        """
        This method logs the user in.
        """
        try:
            request_url = urljoin(check_site(site), self.LOGIN_URL)
        except ValueError:
            raise AuthError(f"Invalid site: {site}")

        response = requests.post(
            request_url,
            json={
                "email": email,
                "password": password,
            },
            headers={
                "Content-Type": "application/json",
            },
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise AuthError(f"Failed to login: {e}")

        data = response.json()

        if "require_2fa" in data:
            raise AuthError("2FA is required")

        # Recover the session cookie
        try:
            session_cookie = response.cookies["swuid"]
        except KeyError:
            raise AuthError("Failed to get session cookie")

        self.__user_data["site"] = check_site(site)
        self.__user_data["session_cookie"] = session_cookie

    def save_session_cookie(self, site: str, cookies: str):
        """
        This method sets the cookies for the SDK.
        """
        # It detects if is a copy-paste from the browser or a simple cookie content

        # First, decode the cookies
        cookies = unquote(cookies).strip()

        if ";" in cookies:
            for cookie in cookies.split(";"):
                if "swuid" in cookie.strip():
                    session_value = cookie.split("swuid")[1].strip()
                    break

        else:
            session_value = cookies.strip()

        self.__user_data["site"] = check_site(site)
        self.__user_data["session_cookie"] = session_value
        self.__keep_user_data__(self.__user_data)

    def get_headers(self, headers: {} = None) -> dict:
        """
        This method returns the headers for the SDK.
        """
        headers = headers or {}

        return {
            "Cookie": f"swuid={self.__user_data['session_cookie']};",
            **headers,
        }

    def __str__(self):
        return f"Auth(site={self.__user_data['site']})"

    @staticmethod
    def __keep_user_data__(user_data: dict):
        """
        This method saves the user data to user profile.
        """
        # Get the user profile path
        user_profile = pathlib.Path.home() / ".ezycourse"

        # Save the user data to the user profile
        with open(user_profile, "w") as f:
            json.dump(user_data, f)

    @staticmethod
    def __restore_user_data__() -> dict:
        """
        This method restores the user data from user profile.
        """
        # Get the user profile path
        user_profile = pathlib.Path.home() / ".ezycourse"

        # Check if the user profile exists
        if not user_profile.exists():
            # Touch the user profile
            user_profile.touch()

        with open(user_profile, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def save(self):
        """
        This method saves the user data.
        """
        self.__keep_user_data__(self.__user_data)
