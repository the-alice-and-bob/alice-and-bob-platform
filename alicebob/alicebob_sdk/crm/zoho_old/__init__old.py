from zohocrmsdk.src.com.zoho.crm.api.exception import SDKException
from zohocrmsdk.src.com.zoho.crm.api.users import UsersOperations
from zohocrmsdk.src.com.zoho.crm.api.util import Constants

# ZOHO_CLIENT_ID="1000.TGMSYJ8A4MIZQ6Z2P0903US5X90OBT"
# ZOHO_CLIENT_SECRET="e3f48d0178038efecac049aab2c1455e72adc9c449"


ZOHO_CLIENT_ID = "1000.TGMSYJ8A4MIZQ6Z2P0903US5X90OBT"
ZOHO_CLIENT_SECRET = "e3f48d0178038efecac049aab2c1455e72adc9c449"

#
# from zohocrmsdk.src.com.zoho.crm.api.request_proxy import RequestProxy
#
#
#
# def get_token_by_id(token_store_file, token_id):
#     file_store = FileStore(token_store_file)
#
#     try:
#         token = file_store.find_token_by_id(token_id)
#         return token
#     except SDKException as ex:
#         # Improved error handling
#         if ex.code == Constants.TOKEN_STORE:
#             print(f"Error retrieving token by ID: {token_id}")
#             print(f"Details: {ex}")
#             # You might want to add logging here for better traceability
#         # Re-raise the exception if necessary
#         raise
#
# class SDKInitializer(object):
#
#     @staticmethod
#     def initialize():
#         # print(get_token_by_id())
#
#
#         logger = Logger.get_instance(level=Logger.Levels.INFO,
#                                      file_path='/tmp/python_sdk_log.log')
#         environment = EUDataCenter.PRODUCTION()
#         # token = OAuthToken(client_id=ZOHO_CLIENT_ID, client_secret=ZOHO_CLIENT_SECRET, grant_token='grant_token',
#         #                    refresh_token="refresh_token", redirect_url='redirectURL')
#
#         # from zohocrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken
#         token = OAuthToken(client_id=ZOHO_CLIENT_ID, client_secret=ZOHO_CLIENT_SECRET, grant_token="grantToken", redirect_url="redirectURL")
#
#
#         store = FileStore(file_path='/tmp/python_sdk_tokens.txt')
#
#         config = SDKConfig(auto_refresh_fields=True, pick_list_validation=False, connect_timeout=None,
#                            read_timeout=None)
#         resource_path = '/tmp/zoho'
#         request_proxy = RequestProxy(host='host', port=9080)
#         # request_proxy = RequestProxy(host='host', port=8080, user='user', password='password')
#         """
#         Call the static initialize method of Initializer class that takes the following arguments
#         2 -> Environment instance
#         3 -> Token instance
#         4 -> TokenStore instance
#         5 -> SDKConfig instance
#         6 -> resource_path
#         7 -> Logger instance. Default value is None
#         8 -> RequestProxy instance. Default value is None
#         """
#         Initializer.initialize(environment=environment, token=token, store=store, sdk_config=config,
#                                resource_path=resource_path, logger=logger, proxy=request_proxy)
#
#
# SDKInitializer.initialize()
from zohocrmsdk.src.com.zoho.crm.api.dc import USDataCenter, EUDataCenter
from zohocrmsdk.src.com.zoho.api.authenticator.store import DBStore, FileStore
from zohocrmsdk.src.com.zoho.api.logger import Logger
from zohocrmsdk.src.com.zoho.crm.api.initializer import Initializer
from zohocrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken
from zohocrmsdk.src.com.zoho.crm.api.sdk_config import SDKConfig
from zohocrmsdk.src.com.zoho.crm.api.request_proxy import RequestProxy

# from zohocrmsdk import SDKConfigBuilder, OAuthToken, InitializeBuilder, USDataCenter, FileStore
# from zohocrmsdk.src.com.zoho.crm.api import Initializer
# from zohocrmsdk.src.com.zoho.crm.api.dc import USDataCenter
# from zohocrmsdk.src.com.zoho.crm.api.users import UsersOperations

# ZohoCRM.modules.ALL,ZohoCRM.users.ALL,ZohoCRM.settings.ALL

ZOHO_CLIENT_ID = "1000.TGMSYJ8A4MIZQ6Z2P0903US5X90OBT"
ZOHO_CLIENT_SECRET = "e3f48d0178038efecac049aab2c1455e72adc9c449"
ZOHO_GRANT_TOKEN = "1000.a23026ca5cdb217d39b75bc686ebbfdc.cb83ec37a176c86a750a8253403f8364"


def initialize_zoho_sdk():
    # Configuración del entorno
    environment = EUDataCenter.PRODUCTION()

    # Crear el token OAuth usando el código de autorización generado
    oauth_token = OAuthToken(
        client_id=ZOHO_CLIENT_ID,
        client_secret=ZOHO_CLIENT_SECRET,
        grant_token=ZOHO_GRANT_TOKEN,
        redirect_url="https://localhost"
    )

    # Configuración del almacenamiento de tokens en un archivo
    file_store = FileStore('./zoho_tokens')  # Directorio donde se guardarán los tokens

    # Configuración del SDK
    config = SDKConfig(auto_refresh_fields=True, pick_list_validation=False, connect_timeout=None,
                       read_timeout=None)

    # config = SDKConfigBuilder().set_auto_refresh_fields(True).set_pick_list_validation(False).build()
    resource_path = './zoho_tokens_data/'  # Directorio para otros recursos del SDK, si es necesario

    # Inicializar el cliente
    Initializer.initialize(
        environment=environment,
        token=oauth_token,
        store=file_store,
        sdk_config=config,
        resource_path=resource_path
    )


# Llama a la función para inicializar el SDK
initialize_zoho_sdk()

from zohocrmsdk.src.com.zoho.crm.api.modules import ModulesOperations


def obtener_modulos():
    modules_operations = ModulesOperations()
    response = modules_operations.get_modules()
    if response is not None:
        response_object = response.get_object()

        for module in response_object.get_modules():
            print(module.get_id())
            print(module.get_module_name())


obtener_modulos()
