import abc
import json
import pathlib

from dataclasses import dataclass
from typing import Protocol, TypeVar, Generic

from urllib.parse import unquote, urljoin

import requests

from awesome_ezycourse import __version__
from .utils import check_site


class AuthError(Exception):
    ...


class AuthLoader(Protocol):
    ...


class AuthSaver(Protocol):
    ...


@dataclass
class UserData:
    email: str | None
    site: str | None
    session_cookie: str | None

    def __str__(self) -> str:
        return f"UserData(email={self.email}, site={self.site})"

    def __repr__(self) -> str:
        return f"<UserData email={self.email}, site={self.site}>"


T = TypeVar("T", bound="Storage")


class Storage[T](Protocol):

    @classmethod
    @abc.abstractmethod
    def make(cls: type[T], user_email: str | None = None, **kwargs) -> T:
        """
        :exception AuthLoader: When the data cannot be saved.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, data: UserData):
        """
        :exception AuthLoader: When the data cannot be saved.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def restore(self) -> UserData:
        """
        :exception AuthLoader: When the data cannot be restored.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError


class FileStorage(Storage):

    def __init__(self, user_email: str | None = None, path: pathlib.Path | str | None = None):
        self.email = user_email
        self.user_profile = path or pathlib.Path.home() / ".ezycourse"

    @classmethod
    def make(cls, user_email: str | None = None, **kwargs) -> "FileStorage":
        return cls(
            user_email=user_email,
            path=kwargs.get("path")
        )

    def save(self, data: UserData):
        """
        This method restores the user data from user profile.
        """

        # Save the user data to the user profile
        with open(self.user_profile, "w") as f:
            json.dump([{
                "email": self.email,
                "site": data.site,
                "session_cookie": data.session_cookie,
            }],
                f
            )

    def restore(self) -> UserData | None:

        # Check if the user profile exists
        if not self.user_profile.exists():
            # Touch the user profile
            self.user_profile.touch()

        with open(self.user_profile, "r") as f:
            try:
                loaded_json = json.load(f)
            except json.JSONDecodeError:
                return None

            if self.email:
                for user in loaded_json:
                    if user["email"] == self.email:
                        return UserData(
                            email=user["email"],
                            site=user["site"],
                            session_cookie=user["session_cookie"],
                        )
                return None

            else:
                # Get the first user
                try:
                    loaded_json = loaded_json[0]
                except IndexError:
                    return None

                return UserData(
                    email=loaded_json["email"],
                    site=loaded_json["site"],
                    session_cookie=loaded_json["session_cookie"],
                )

    def __str__(self) -> str:
        return f"FileStorage(path={self.user_profile})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} path={self.user_profile}>"


class Auth:
    """
    This class manages the authentication configuration for the SDK.
    """
    LOGIN_URL = "/api/student/auth/login"

    def __init__(self, storage: Storage = None):
        """
        This method initializes the SDK.
        """
        self.__storage = storage or FileStorage()
        self.__user_data: UserData | None = None

    @property
    def is_logged(self) -> bool:
        """
        This method returns whether the user is logged in.
        """
        if not self.__user_data:
            return False

        if not self.__user_data.site or not self.__user_data.session_cookie:
            return False

        return True

    @property
    def site(self) -> str:
        """
        This method returns the site for the SDK.
        """
        if not self.__user_data:
            raise AuthError("User data is not set")

        if not self.__user_data.site:
            raise AuthError("Site is not set")

        return self.__user_data.site

    @property
    def session_cookie(self) -> str:
        """
        This method returns the session cookie for the SDK.
        """
        if not self.__user_data:
            raise AuthError("User data is not set")

        if not self.__user_data.session_cookie:
            raise AuthError("Session cookie is not set")

        return self.__user_data.session_cookie

    def restore(self):
        """
        This method restores the user data from user profile.
        """
        restored_data = self.__storage.restore()

        if restored_data:
            self.__user_data = restored_data

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

        self.__user_data = UserData(
            email=email,
            site=check_site(site),
            session_cookie=session_cookie
        )

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
                raise AuthError("Session cookie not found")

        else:
            session_value = cookies.strip()

        self.__user_data.site = check_site(site)
        self.__user_data.session_cookie = session_value

        self.__storage.save(self.__user_data)

    def get_headers(self, headers: {} = None, include_banner: bool = True) -> dict:
        """
        This method returns the headers for the SDK.
        """
        headers = headers or {}

        if include_banner:
            headers["User-Agent"] = f"EzyCourse SDK Client/{__version__}"

        return {
            "Cookie": f"swuid={self.__user_data.session_cookie};",
            **headers,
        }

    def __str__(self):
        return f"Auth(site={self.__user_data.site})"

    def save(self):
        """
        This method saves the user data.
        """
        self.__storage.save(self.__user_data)


__all__ = ("Auth", "AuthError", "AuthLoader", "AuthSaver", "FileStorage", "Storage", "UserData")
