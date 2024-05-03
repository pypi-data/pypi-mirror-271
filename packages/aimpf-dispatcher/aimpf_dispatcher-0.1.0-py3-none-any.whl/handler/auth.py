from __future__ import annotations

import os
import boto3
import json
import logging
import requests
from pycognito.aws_srp import AWSSRP
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("DEBUG_LEVEL", "INFO"))


__all__ = ["AuthorizationAgent"]


class AuthorizationAgent:
    def __init__(self, username: str | None=None, password: str | None=None, *, token: str | None=None, url: str | None=None):
        """
        Either a username/password or a token must be provided.

        Parameters
        ----------
        username : str
            Carta username.
        password : str
            Carta password.

        token : str
            If provided, token supercedes username/password.
        url : str
            Base URL for API calls.
        """
        self.url = str(url or "https://api.carta.contextualize.us.com")
        try:
            self.url = str(url) or os.environ["CARTA_AUTH_URL"]
        except KeyError:
            raise ValueError("A valid API URL must be provided.")
        logger.debug(f"Creating AuthenticationAgent to access {self.url!r}.")
        self.__username = None
        self.__token = None
        self.__session = requests.Session()
        if not token:
            if username and password:
                self.password_authentication(username, password)
            else:
                raise ValueError(f"No authentication information was provided.")
        else:
            try:
                token = json.loads(token)
            except json.JSONDecodeError:
                pass
            self.__token = str(token).replace("Bearer ", "")
            self.__session.headers.update({"Authorization": f"Bearer {self.__token}"})

    @staticmethod
    def __raise(exception: Exception, message: str):
        raise exception(message)
    
    @property
    def token(self):
        return self.__token

    # Getter/setter for username.
    username = property(
        lambda self: self.__username,
        lambda self, value: AuthorizationAgent.__raise(
            AttributeError,
            "Cannot set 'username' directly. Use `AuthorizationAgent.password_authentication`.")
    )

    def is_authenticated(self) -> bool:
        return (not self.__token)
    
    def password_authentication(self, username: str, password: str) -> None:
        """
        Performs username/password-based authentication.

        Parameters
        ----------
        username : str
            Carta user name.
        password : str
            Carta password.

        Returns
        -------
        None
        """
        class PoolModel(BaseModel, extra="allow"):
            # Ensure the Authenticator response contains the data we need.
            id: str = Field(alias="userPoolId")
            region: str
            clientId: str = Field(alias="userPoolWebClientId")

        class AuthModel(BaseModel, extra="allow"):
            # Ensure the Authorization call has the data we need.
            class TokenModel(BaseModel, extra="allow"):
                token: str = Field(alias="IdToken")
            auth: AuthModel.TokenModel = Field(alias="AuthenticationResult")

        logger.debug("Getting information to authenticate.")
        response = requests.get(
            url=f"{self.url}/auth"
        )
        pool = PoolModel(**json.loads(response.content))
        logger.debug(f"Pool: (id, region, clientId) = " \
                     f"({pool.id}, {pool.region}, {pool.clientId}).")
        client = boto3.client("cognito-idp", region_name=pool.region)
        aws = AWSSRP(
            username=str(username),
            password=str(password),
            pool_id=pool.id,
            client_id=pool.clientId,
            client=client
        )
        logger.debug(f"Authenticating {str(username)!r}.")
        auth = AuthModel(**aws.authenticate_user())
        self.__username = str(username)
        self.__token = str(auth.auth.token)
        self.__session.headers.update({"Authorization": f"Bearer {self.__token}"})
    
    # Mimic the requests API
    def _get_url(self, endpoint: str) -> str:
        url = str(self.url) + "/" + str(endpoint).strip("/")
        logger.debug(f"URL: {url}")
        return url
    
    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        logger.debug(f"Calling request {method!r}.")
        return self.__session.request(str(method), self._get_url(endpoint), **kwargs)
    
    def head(self, endpoint: str, **kwargs) -> requests.Response:
        logger.debug(f"Calling 'head'.")
        return self.__session.head(self._get_url(endpoint), **kwargs)
    
    def get(self, endpoint: str, params=None, **kwargs) -> requests.Response:
        logger.debug(f"Calling 'get' with params: {params}.")
        return self.__session.get(self._get_url(endpoint), params=params, **kwargs)
    
    def post(self, endpoint: str, data=None, json=None, **kwargs) -> requests.Response:
        logger.debug(f"Calling 'post' with " \
                     f"data: {'Y' if data else 'N'}, " \
                     f"json: {'Y' if json else 'N'}.")
        return self.__session.post(self._get_url(endpoint),
                                   data=data, json=json, **kwargs)
    
    def put(self, endpoint: str, data=None, **kwargs) -> requests.Response:
        logger.debug(f"Calling 'put' with data: {'Y' if data else 'N'}.")
        return self.__session.put(self._get_url(endpoint), data=data, **kwargs)
    
    def patch(self, endpoint: str, data=None, **kwargs) -> requests.Response:
        logger.debug(f"Calling 'patch' with data: {'Y' if data else 'N'}.")
        return self.__session.patch(self._get_url(endpoint), data=data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        logger.debug(f"Calling 'delete'.")
        return self.__session.delete(self._get_url(endpoint), **kwargs)
