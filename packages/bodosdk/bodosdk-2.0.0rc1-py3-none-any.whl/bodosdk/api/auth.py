from datetime import datetime

import jwt

from bodosdk.api.request_wrapper import RequestWrapper
from bodosdk.exceptions import Unauthorized
from bodosdk.base import APIKeys


class AuthApi:
    def __init__(
        self,
        auth: APIKeys,
        auth_url="https://auth.bodo.ai",
        requests=RequestWrapper(),
    ):
        self._requests = requests
        self._auth_url = auth_url
        self._auth = auth
        self._token = None

    def _authenticate(self):
        resp = self._requests.post(
            f"{self._auth_url}/identity/resources/auth/v2/api-token",
            json={
                "clientId": self._auth.client_id,
                "secret": self._auth.secret_key,
            },
        )
        if resp.status_code == 200:
            return resp.json()["access_token"]
        raise Unauthorized(
            "Authentication failed. Suggestion: check Client ID and Secret Key values."
        )

    def switch_workspace(self, auth: APIKeys):
        self._auth = auth
        self._token = self._authenticate()

    @property
    def auth_token(self):
        if self._token is not None:
            try:
                exp = datetime.fromtimestamp(self.decode_token(self._token)["exp"])
                if exp < datetime.now():
                    self._token = self._authenticate()
            except Exception as ex:  # noqa: F841
                self._token = self._authenticate()
        else:
            self._token = self._authenticate()
        return self._token

    def decode_token(self, token):
        return jwt.decode(token, options={"verify_signature": False})
