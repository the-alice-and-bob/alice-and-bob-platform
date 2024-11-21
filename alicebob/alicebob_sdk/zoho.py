from awesome_zohocrm.entrypoint import ZohoCRM
from awesome_zohocrm.auth import AuthenticationStorage, AuthException, Auth

from zoho.models import ZohoOAuth


class DjangoAuthenticationStorage(AuthenticationStorage):

    def get_auth_data(self) -> dict:
        try:
            auth = ZohoOAuth.objects.first()
            return {
                "client_id": auth.client_id,
                "client_secret": auth.client_secret,
                "refresh_token": auth.refresh_token,
                "grant_token": auth.grant_token,
                "expires_in": auth.expiry_time,
                "access_token": auth.access_token
            }
        except Exception as e:
            raise AuthException(f"Error getting auth data: {str(e)}")

    def save_auth_data(self, client_id: str, client_secret: str, refresh_token: str, grant_token: str, expires_in: int, access_token: str):
        try:
            ZohoOAuth.objects.update_or_create(
                defaults={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "refresh_token": refresh_token,
                    "grant_token": grant_token,
                    "expiry_time": expires_in,
                    "access_token": access_token
                }
            )
        except Exception as e:
            raise AuthException(f"Error saving auth data: {str(e)}")


def zoho_instance() -> ZohoCRM:
    auth = Auth(auth_storage=DjangoAuthenticationStorage())

    return ZohoCRM(auth=auth)


__all__ = ("zoho_instance",)
