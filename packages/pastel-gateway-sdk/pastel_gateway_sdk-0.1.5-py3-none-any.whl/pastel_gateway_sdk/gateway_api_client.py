from pastel_gateway_sdk.api import (LoginApi, AccountApi, ApiKeysApi, UsersApi,
                                    CascadeApi, CollectionApi, NftApi, SenseApi,
                                    AdminApi, KeyAuthApi)
from pastel_gateway_sdk import ApiClient, Configuration, Token


class GatewayApiClientAsync(ApiClient):
    NETWORKS = {
        "mainnet": "https://gateway-api.pastel.network/",
        "testnet": "https://testnet.gateway-api.pastel.network/",
        "devnet": "https://devnet.gateway-api.pastel.network/"
    }

    def __init__(self, network: str = None, custom_url: str = None):
        self.host = self.get_host(network, custom_url)
        configuration = Configuration(host=self.host)
        super().__init__(configuration)

        self._token = None
        self._account_api = None
        self._api_keys_api = None
        self._users_api = None
        self._login_api = None
        self._cascade_api = None
        self._collection_api = None
        self._nft_api = None
        self._sense_api = None
        self._admin_api = None
        self._key_auth_api = None

    @staticmethod
    def get_host(network, custom_url):
        if custom_url is not None:
            return custom_url
        if network in GatewayApiClientAsync.NETWORKS:
            return GatewayApiClientAsync.NETWORKS[network]
        raise ValueError(f"Invalid network. Choose from {list(GatewayApiClientAsync.NETWORKS.keys())} "
                         f"or provide custom_url")

    async def authenticate(self, username: str, password: str) -> bool:
        login_api = self.login_api
        token = await login_api.login_access_token(username=username, password=password)
        if not token or type(token) is not Token or not token.access_token:
            return False
        self.set_token(token.access_token)
        return True

    def set_token(self, token: str | None):
        self.configuration.access_token = token
        self._token = token

    async def logout(self):
        self.clear_auth_api_key()
        self.set_token(None)
        self._account_api = None
        self._api_keys_api = None
        self._users_api = None
        self._login_api = None
        self._cascade_api = None
        self._collection_api = None
        self._nft_api = None
        self._sense_api = None
        self._admin_api = None
        self._key_auth_api = None

    async def test_token(self):
        api = self.login_api
        user = await api.login_test_token()
        return user

    def set_auth_api_key(self, api_key):
        self.configuration.api_key["APIKeyHeader"] = api_key

    def clear_auth_api_key(self):
        self.configuration.api_key.pop("APIKeyHeader", None)

    @property
    def login_api(self):
        if self._login_api is None:
            self._login_api = LoginApi(self)
        return self._login_api

    @property
    def account_api(self):
        if self._token is None:
            raise ValueError("Please authenticate before accessing this API.")
        if self._account_api is None:
            self._account_api = AccountApi(self)
        return self._account_api

    @property
    def api_keys_api(self):
        if self._token is None:
            raise ValueError("Please authenticate before accessing this API.")
        if self._api_keys_api is None:
            self._api_keys_api = ApiKeysApi(self)
        return self._api_keys_api

    @property
    def users_api(self):
        if self._token is None:
            raise ValueError("Please authenticate before accessing this API.")
        if self._users_api is None:
            self._users_api = UsersApi(self)
        return self._users_api

    @property
    def cascade_api(self):
        if self._cascade_api is None:
            self._cascade_api = CascadeApi(self)
        return self._cascade_api

    @property
    def collection_api(self):
        if self._collection_api is None:
            self._collection_api = CollectionApi(self)
        return self._collection_api

    @property
    def nft_api(self):
        if self._nft_api is None:
            self._nft_api = NftApi(self)
        return self._nft_api

    @property
    def sense_api(self):
        if self._sense_api is None:
            self._sense_api = SenseApi(self)
        return self._sense_api

    @property
    def admin_api(self):
        if self._admin_api is None:
            self._admin_api = AdminApi(self)
        return self._admin_api

    @property
    def key_auth_api(self):
        if self._key_auth_api is None:
            self._key_auth_api = KeyAuthApi(self)
        return self._key_auth_api
