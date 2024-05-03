import pytest
import unittest
import urllib3
import uuid

from pynpdc.auth import AccessLevel, Account, AccountWithToken, AuthClient
from pynpdc.exception import APIException
from .config import get_config

"""
Prerequisites for this test suite:

- a user foo@example.org with password 1234123412341234 has to exist.
- an admin user admin@example.org with password 1234123412341234 has to exist.
"""

BAD_TOKEN = "0000111122223333444455556666777788889999aaaabbbbccccddddeeeeffff"


@pytest.fixture(scope="class")
def run_fixtures(request):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    cfg = get_config()

    request.cls.entrypoint = cfg["komainu"]["entrypoint"]
    request.cls.user = cfg["komainu"]["testUser"]
    request.cls.password = cfg["komainu"]["testPassword"]
    request.cls.admin_user = cfg["komainu"]["testAdminUser"]
    request.cls.admin_password = cfg["komainu"]["testAdminPassword"]

    request.cls.client = AuthClient(request.cls.entrypoint, verify_ssl=False)


class TestAccountWithToken(unittest.TestCase):
    def test_update_token(self):
        account = AccountWithToken({"token": "123"})
        self.assertEqual(account.token, "123")

        account.token = "124"
        self.assertEqual(account.token, "124")


@pytest.mark.usefixtures("run_fixtures")
class TestAuth(unittest.TestCase):
    def setUp(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def test_login_succeeds(self):
        account = self.client.login(self.user, self.password)
        self.assertEqual(account.email, self.user)
        self.assertIsInstance(account.token, str)
        self.assertNotEqual(account.token, "")
        self.assertIsInstance(account.id, str)
        self.assertNotEqual(account.id, "")
        self.assertIsInstance(account.access_level, AccessLevel)

    def test_login_fails(self):
        with pytest.raises(APIException) as e_info:
            self.client.login("not-a-user@example.org", "random-password")

        e = e_info.value
        self.assertEqual(e.status_code, 401)

    def test_logout(self):
        account = self.client.login(self.user, self.password)
        self.client.logout(account)

        with pytest.raises(APIException):
            self.client.logout(account)

    def test_logout_with_bad_token_fails(self):
        account = AccountWithToken({"token": BAD_TOKEN})

        with pytest.raises(APIException) as e_info:
            self.client.logout(account)

        e = e_info.value
        self.assertEqual(e.status_code, 401)

    def test_get_account(self):
        login_account = self.client.login(self.user, self.password)
        account_id = login_account.id

        account = self.client.get_account(account_id)

        self.assertIsInstance(account, Account)
        self.assertEqual(account.id, account_id)
        self.assertEqual(account.email, self.user)
        self.assertIsInstance(account.access_level, AccessLevel)

    def test_getting_non_existent_account_fails(self):
        account_id = uuid.uuid4()
        account = self.client.get_account(account_id)
        self.assertIsNone(account)

    def test_authorize(self):
        login_account = self.client.login(self.user, self.password)

        account = self.client.authorize(login_account.token)

        self.assertIsInstance(account, Account)
        self.assertEqual(account.id, login_account.id)
        self.assertEqual(account.email, self.user)
        self.assertIsInstance(account.access_level, AccessLevel)

    def test_authorizing_with_bad_token_fails(self):
        with pytest.raises(APIException) as e_info:
            self.client.authorize(BAD_TOKEN)

        e = e_info.value
        self.assertEqual(e.status_code, 401)

    def test_keepalive(self):
        login_account = self.client.login(self.user, self.password)

        token = self.client.keepalive(login_account)

        self.assertIsInstance(token, str)
        self.assertNotEqual(token, login_account.token)

    def test_calling_keepalive_with_bad_token_fails(self):
        account = AccountWithToken({"token": BAD_TOKEN})

        with pytest.raises(APIException) as e_info:
            self.client.keepalive(account)

        e = e_info.value
        self.assertEqual(e.status_code, 401)

    def test_changing_password_fails_with_invalid_new_current_password(self):
        # We do not want to mess with existing accounts, so therefore we only
        # test an error case, that will not change the password.

        login_account = self.client.login(self.user, self.password)

        with pytest.raises(APIException) as e_info:
            self.client.change_password(login_account, self.password, "too-short")

        e = e_info.value
        self.assertEqual(e.status_code, 422)
        issue_field = e.response.json()["details"]["issues"][0]["field"]
        self.assertEqual(issue_field, "newPassword")

    def test_account_administration(self):
        """
        This function tests both create_account and update_account.

        Normally we keep the tests separated, but since it is not possible to
        delete accounts through the API we want to create accounts as little as
        possible in the unit tests.
        """

        # create_account
        # --------------

        originator_account = self.client.login(self.admin_user, self.admin_password)
        new_account_email = f"test-{uuid.uuid4()}@example.org"

        account = self.client.create_account(originator_account, new_account_email)

        self.assertEqual(account.email, new_account_email)
        self.assertEqual(account.access_level, AccessLevel.EXTERNAL)
        self.assertFalse(account.directory_user)
        self.assertGreater(len(account.password), 0)

        # check if it is possible to login with the new account

        logged_in_account = self.client.login(new_account_email, account.password)

        self.assertEqual(logged_in_account.email, new_account_email)
        self.assertEqual(logged_in_account.access_level, AccessLevel.EXTERNAL)
        self.assertFalse(logged_in_account.directory_user)

        # update_account
        # --------------

        self.client.update_account(originator_account, account.id, active=False)

        # now login should not be possible anymore

        with pytest.raises(APIException) as e_info:
            self.client.login(new_account_email, account.password)

        e = e_info.value
        self.assertEqual(e.status_code, 401)

    def test_creating_an_account_without_admin_level_fails(self):
        originator_account = self.client.login(self.user, self.password)
        new_account_email = f"test-{uuid.uuid4()}@example.org"

        with pytest.raises(APIException) as e_info:
            self.client.create_account(originator_account, new_account_email)

        e = e_info.value
        self.assertEqual(e.status_code, 403)

    def test_updating_an_account_without_admin_level_fails(self):
        account = self.client.login(self.user, self.password)
        account_id = account.id

        with pytest.raises(APIException) as e_info:
            self.client.update_account(account, account_id, active=False)

        e = e_info.value
        self.assertEqual(e.status_code, 403)
