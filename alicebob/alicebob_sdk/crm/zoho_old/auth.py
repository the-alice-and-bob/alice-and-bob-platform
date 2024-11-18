import tempfile

from zohocrmsdk.src.com.zoho.crm.api.dc import EUDataCenter
from zohocrmsdk.src.com.zoho.crm.api.sdk_config import SDKConfig
from zohocrmsdk.src.com.zoho.crm.api.initializer import Initializer
from zohocrmsdk.src.com.zoho.api.authenticator.store import FileStore
from zohocrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken


def initialize_zoho_sdk(zoho_client_id, zoho_client_secret, zoho_grant_token, token_path, resource_path: str = None):

    # Configuración del entorno
    environment = EUDataCenter.PRODUCTION()

    # Crear el token OAuth usando el código de autorización generado
    oauth_token = OAuthToken(
        client_id=zoho_client_id,
        client_secret=zoho_client_secret,
        grant_token=zoho_grant_token,
        # refresh_token=zoho_grant_token,
        redirect_url="https://localhost"
    )

    # Configuración del almacenamiento de tokens en un archivo
    file_store = FileStore(token_path)

    # Configuración del SDK
    config = SDKConfig(auto_refresh_fields=True, pick_list_validation=False, connect_timeout=None, read_timeout=None)

    resource_path = resource_path or tempfile.gettempdir()

    # Inicializar el cliente
    Initializer.initialize(
        environment=environment,
        token=oauth_token,
        store=file_store,
        sdk_config=config,
        resource_path=resource_path
    )

