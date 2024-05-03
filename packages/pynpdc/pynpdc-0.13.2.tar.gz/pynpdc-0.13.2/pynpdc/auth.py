from __future__ import annotations
import base64
import requests
from typing import Optional

from .exception import APIException
from .types import (
    AccessLevel,
    AccountAPIResponse,
    AccountWithPasswordAPIResponse,
    AccountWithTokenAPIResponse,
    KeepaliveAPIResponse,
)

AUTH_STAGING_ENTRYPOINT = "https://beta.data.npolar.no/-/auth/"
AUTH_LIFE_ENTRYPOINT = "https://auth.data.npolar.no/"


class Account:
    """
    A basic account object.

    Attributes:
        raw (AccountAPIResponse): The API response data parsed from JSON
        client (AuthClient | None) The client for the auth module
    """

    raw: AccountAPIResponse
    client: Optional[AuthClient]

    def __init__(
        self, raw: AccountAPIResponse, *, client: Optional[AuthClient] = None
    ) -> None:
        """
        Initialize an instance of rhe Account model class.

        Args:
            raw (AccountAPIResponse): The API response as parsed JSON
            client (AuthClient): The used auth client
        """
        self.raw = raw
        self.client = client

    @property
    def access_level(self) -> AccessLevel:
        """
        Retrieve the access level of the account.

        Returns:
            AccessLevel: the access level of the account
        """

        level = self.raw["accessLevel"]
        return AccessLevel(level)

    @property
    def email(self) -> str:
        """
        Retrieve the email.

        Returns:
            str: the email used for login
        """
        return self.raw["email"]

    @property
    def id(self) -> str:
        """
        Retrieve the id.

        Returns:
            str: the id as UUID
        """
        return self.raw["id"]

    @property
    def directory_user(self) -> bool:
        """
        Retrieve a flag that indicates whether the account is managed by AD

        Returns:
            bool: the AD flag
        """
        return self.raw["directoryUser"]


class AccountWithToken(Account):
    """
    A logged in account with token.

    Attributes:
        raw (AccountWithTokenAPIResponse): The API response data parsed from JSON
        client (AuthClient | None) The client for the auth module
    """

    raw: AccountWithTokenAPIResponse

    @property
    def token(self) -> str:
        """
        Retrieve the login token.

        Returns:
            str: the login token
        """
        return self.raw["token"]

    @token.setter
    def token(self, token: str) -> None:
        """
        Replace token value

        Args:
            token (str): The new token

        """
        self.raw["token"] = token


class AccountWithCleartextPassword(Account):
    """
    An freshly created Account with cleartext password.

    Attributes:
        raw (AccountWithPasswordAPIResponse): The API response data parsed from JSON
        client (AuthClient | None) The client for the auth module
    """

    raw: AccountWithPasswordAPIResponse

    @property
    def password(self) -> str:
        """
        Retrieve the cleartext password after account creation by an admin.

        Returns:
            str: the cleartext password
        """
        return self.raw["password"]


class AuthClient:
    entrypoint: str
    verify_ssl: bool

    """
    A client to communicate with the NPDC auth module.

    Attributes:
        entrypoint (str): The entrypoint of the Rest API with a trailing slash
        verify_ssl (bool): Set to false, when the Rest API has a self signed
            certificate
    """

    def __init__(self, entrypoint: str, *, verify_ssl: bool = True) -> None:
        """
        Create a new AuthClient.

        Args:
            entrypoint (str): The entrypoint of the Rest API with a trailing
                slash
            verify_ssl (bool): Set to false, when the Rest API has a self signed
                certificate
        """
        self.entrypoint = entrypoint
        self.verify_ssl = verify_ssl

    def login(self, email: str, password: str) -> AccountWithToken:
        """
        Login a user and retrieve account.

        Args:
            email (str): The user email
            password (str): The user password

        Returns:
            AccountWithToken: The logged in account

        Raises:
            APIException: if the HTTP status code of the response is not 200
        """
        creds = base64.b64encode(bytes(f"{email}:{password}", "utf8"))
        endpoint = f"{self.entrypoint}authenticate/"
        headers = {"Authorization": "Basic " + creds.decode("utf8")}

        response = requests.get(endpoint, headers=headers, verify=self.verify_ssl)
        if response.status_code != 200:
            raise APIException(response)

        return AccountWithToken(response.json(), client=self)

    def logout(self, account: AccountWithToken) -> None:
        """
        Logout a user.

        Args:
            account (AccountWithToken): The account to log out

        Raises:
            APIException: if the HTTP status code of the response is not 200
        """
        endpoint = f"{self.entrypoint}authenticate/"
        headers = {"Authorization": f"Bearer {account.token}"}

        response = requests.delete(endpoint, headers=headers, verify=self.verify_ssl)
        if response.status_code != 200:
            raise APIException(response)

    def authorize(self, token: str) -> Account:
        """
        Retrieve a logged in account by token

        Args:
            token (str): the account.token property received from the login
                method

        Returns:
            Account

        Raises:
            APIException: if the HTTP status code of the response is not 200
        """

        endpoint = f"{self.entrypoint}authorize/"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(endpoint, headers=headers, verify=self.verify_ssl)

        if response.status_code != 200:
            raise APIException(response)

        return Account(response.json())

    def create_account(
        self, originator_account: AccountWithToken, email: str
    ) -> AccountWithCleartextPassword:
        """
        Create a new external account

        Only admins have access to this method

        Args:
            originator_account (AccountWithToken ): the account used to create the new
                account. Has to have accessLevel admin.
            email (str): the email for the account. The email domain must not be
                an internal one (npolar.no in the production system)

        Returns:
            AccountWithCleartextPassword

        Raises:
            APIException: if the HTTP status code of the response is not 201
        """

        endpoint = f"{self.entrypoint}account/"
        headers = {"Authorization": f"Bearer {originator_account.token}"}
        payload = {"email": email}
        response = requests.post(
            endpoint, headers=headers, json=payload, verify=self.verify_ssl
        )

        if response.status_code != 201:
            raise APIException(response)

        return AccountWithCleartextPassword(response.json())

    def get_account(self, account_id: str) -> Account | None:
        """
        Retrieve an account by ID

                When the account is not found, None is returned.

        Args:
            account_id (str): the UUID of the account

        Returns:
            Account | None

        Raises:
            APIException: if the HTTP status code of the response is 500
        """

        endpoint = f"{self.entrypoint}account/{account_id}"
        response = requests.get(endpoint, verify=self.verify_ssl)

        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise APIException(response)

        return Account(response.json())

    def update_account(
        self, originator_account: AccountWithToken, account_id: str, *, active: bool
    ) -> Account:
        """
        Update an external account

        Only admins have access to this method

        Args:
            originator_account (AccountWithToken): the account used to update
                the account. Has to have accessLevel admin.
            account_id (str): the UUID of the account
            active (bool): the active set to be updated in the account

        Returns:
            Account

        Raises:
            APIException: if the HTTP status code of the response is not 200
        """

        endpoint = f"{self.entrypoint}account/{account_id}"
        headers = {"Authorization": f"Bearer {originator_account.token}"}
        payload = {"active": active}
        response = requests.put(
            endpoint, headers=headers, json=payload, verify=self.verify_ssl
        )

        if response.status_code != 200:
            raise APIException(response)

        return Account(response.json())

    def change_password(
        self, account: AccountWithToken, current_password: str, new_password: str
    ) -> None:
        endpoint = f"{self.entrypoint}account/"
        headers = {"Authorization": f"Bearer {account.token}"}
        payload = {
            "currentPassword": current_password,
            "newPassword": new_password,
        }

        response = requests.put(
            endpoint, headers=headers, json=payload, verify=self.verify_ssl
        )
        if response.status_code > 204:
            raise APIException(response)

    def keepalive(self, account: AccountWithToken) -> str:
        """
        Extend the login session and retrieve a new token

        Args:
            account (AccountWithToken): the account that should be extended. Has
                to have a valid token

        Returns:
            str

        Raises:
            APIException: if the HTTP status code of the response is not 200
        """
        endpoint = f"{self.entrypoint}keepalive/"
        headers = {"Authorization": f"Bearer {account.token}"}

        response = requests.post(endpoint, headers=headers, verify=self.verify_ssl)

        if response.status_code != 200:
            raise APIException(response)

        response_data: KeepaliveAPIResponse = response.json()
        return response_data["token"]
