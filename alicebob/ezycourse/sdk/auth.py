from abc import ABC

from django.conf import settings

from awesome_ezycourse.sdk.auth import AuthError, Storage, Auth, UserData

from ..models import EzyCourseAuth


class DjangoAuthentication(Storage, ABC):

    @classmethod
    def make(cls, user_email: str | None = None, **kwargs):
        return cls(user_email=user_email)

    def __repr__(self):
        return f"<DjangoAuthentication user_email={self.user_email}>"

    def __str__(self):
        return f"<DjangoAuthentication user_email={self.user_email}>"

    def __init__(self, user_email: str | None = None):
        self.user_email = user_email

    def save(self, data: UserData):
        try:
            auth = EzyCourseAuth.objects.get(email=self.user_email)

            auth.site = data.site
            auth.session_cookie = data.session_cookie
            auth.email = self.user_email
            auth.save()

        except EzyCourseAuth.DoesNotExist:

            EzyCourseAuth.objects.create(
                site=data.site,
                session_cookie=data.session_cookie,
                email=self.user_email
            )

    def restore(self) -> UserData:
        try:
            if self.user_email:
                auth = EzyCourseAuth.objects.get(email=self.user_email)

            else:
                auth = EzyCourseAuth.objects.first()

            return UserData(
                email=auth.email,
                site=auth.site,
                session_cookie=auth.session_cookie
            )

        except Exception as e:
            raise AuthError(f"Error getting auth data: {str(e)}")


def ezycourse_instance(email: str | None = None) -> Auth:
    if not email:
        email = settings.EZYCOURSE_ADMIN_EMAIL

    auth = Auth(storage=DjangoAuthentication.make(user_email=email))
    auth.restore()

    return auth


__all__ = ("ezycourse_instance",)
