import re
from typing import List, Optional

from django.contrib.auth.models import User
from django.test import TransactionTestCase
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.models import ClientAccount, ClientWallet, ClientWalletTransaction


# api.tests.ClientAccountApiTests.test_create_regular_user_and_sign_in
class CommonApiTests(APITestCase):
    default_user_username = 'testuser'
    default_user_password = 'aaa'

    def create_user_auth(
        self, username: str = default_user_username, password: str = default_user_password,
        is_staff: bool = False
    ) -> User:
        """
        Create a User
        """
        user, is_created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.is_staff = is_staff
        user.is_active = True
        user.is_superuser = False
        user.save()
        return user

    def create_client_account(
        self, name: Optional[str] = default_user_username,
        surname: Optional[str] = default_user_username,
        user_account: User = None,
        **kwargs: object
    ) -> Optional[ClientAccount]:
        if user_account:
            return ClientAccount.objects.create(
                name=name, surname=surname, user_account=user_account, **kwargs
            )
        return None

    def create_client_wallet(
        self, client_account: ClientAccount, **kwargs: object
    ) -> Optional[ClientWallet]:
        return ClientWallet.objects.create(
            client_account=client_account, **kwargs
        )

    def create_client_transaction(
        self, amount: float, client_wallet: ClientWallet, **kwargs: object
    ) -> ClientWalletTransaction:
        return ClientWalletTransaction.objects.create(
            amount=amount,
            client_wallet_account=client_wallet, **kwargs
        )

    def set_url(self, name: str, kwargs: object = None) -> None:
        self.url = reverse(name, kwargs=kwargs)
        self.full_url = 'http://testserver' + self.url

    def normalize_username(self, text: str = '') -> str:
        """
        This method receive a str and remove whitespaces
        """
        return re.sub(r'\s+', '_', text)

    def generate_name_and_surname(self, faker_instance: Faker) -> List[str]:
        """
        This method generates a first and last name
        """
        name = self.normalize_username(faker_instance.unique.first_name())
        surname = self.normalize_username(faker_instance.unique.last_name())
        return [name, surname]


class UserApiTests(CommonApiTests):
    fake = None

    def setUp(self) -> None:
        """
        Config

        * Docs
        ** Faker
        *** Examples: https://faker.readthedocs.io/en/stable/fakerclass.html#examples
        *** Unique values: https://faker.readthedocs.io/en/stable/fakerclass.html#unique-values
        :return:
        """
        self.fake = Faker()

        super().setUp()

    def test_create_regular_user_and_sign_in(self):
        username_password = self.fake.unique.name().lower().replace(' ', '_')
        payload = {
            "username": username_password,
            "password": username_password,
            "email": ''
        }
        response_data = {
            'username': username_password,
            'first_name': '',
            'last_name': '',
            'email': '',
            'is_staff': False
        }
        self.set_url('api:user_api-list')
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(201, response.status_code)

        response_data_unique_items = set(response_data.items())
        response_json_unique_items = set(response.json().items())
        self.assertTrue(response_data_unique_items.issubset(response_json_unique_items))

        self.assertTrue(
            self.client.login(username=payload.get('username'), password=payload.get('password')),
            msg='Login error'
        )

    def test_create_staff_user_and_sign_in(self):
        username_password = self.fake.unique.name().lower().replace(' ', '_')
        payload = {
            "username": username_password,
            "password": username_password,
            "email": '',
            "is_staff": True
        }
        response_data = {
            'username': username_password,
            'first_name': '',
            'email': '',
            'is_staff': True
        }
        self.set_url('api:user_api-list')
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(201, response.status_code)

        response_data_unique_items = set(response_data.items())
        response_json_unique_items = set(response.json().items())
        self.assertTrue(response_data_unique_items.issubset(response_json_unique_items))

        self.assertTrue(
            self.client.login(username=payload.get('username'), password=payload.get('password')),
            msg='Login error'
        )

    def test_update_regular_user(self):
        username_password = self.fake.unique.name().lower().replace(' ', '_')
        user = self.create_user_auth(
            username=username_password, password=username_password
        )
        self.client.login(
            username=username_password, password=username_password
        )
        api_url_params = {
            "pk": user.id
        }
        payload = {
            "first_name": username_password,
            "last_name": username_password,
            "email": f'{username_password}@foobar.com.es',
        }
        response_data = {
            "username": username_password,
            "first_name": username_password,
            "last_name": username_password,
            "email": f"{username_password}@foobar.com.es",
            "is_staff": False
        }
        self.set_url('api:user_api-detail', kwargs=api_url_params)
        response = self.client.patch(self.url, data=payload, format='json')
        self.assertEqual(200, response.status_code)

        response_data_unique_items = set(response_data.items())
        response_json_unique_items = set(response.json().items())
        self.assertTrue(response_data_unique_items.issubset(response_json_unique_items))

    def test_update_staff_user(self):
        username_password = self.fake.unique.name().lower().replace(' ', '_')
        user = self.create_user_auth(
            username=username_password, password=username_password, is_staff=True
        )
        self.client.login(
            username=username_password, password=username_password
        )
        api_url_params = {
            "pk": user.id
        }
        payload = {
            "first_name": username_password,
            "last_name": username_password,
            "email": f'{username_password}@foobar.com.es',
        }
        response_data = {
            "username": username_password,
            "first_name": username_password,
            "last_name": username_password,
            "email": f"{username_password}@foobar.com.es",
            "is_staff": True
        }
        self.set_url('api:user_api-detail', kwargs=api_url_params)

        response = self.client.patch(self.url, data=payload, format='json')
        self.assertEqual(200, response.status_code)

        response_data_unique_items = set(response_data.items())
        response_json_unique_items = set(response.json().items())
        self.assertTrue(response_data_unique_items.issubset(response_json_unique_items))


class ClientAccountApiTests(CommonApiTests):
    fake = None
    regular_user = None
    staff_user = None
    regular_user_account = None
    staff_user_account = None
    staff_user_username = 'test_staff'

    def setUp(self):
        """
        Config

        * Docs
        ** Faker
        *** Examples: https://faker.readthedocs.io/en/stable/fakerclass.html#examples
        *** Unique values: https://faker.readthedocs.io/en/stable/fakerclass.html#unique-values
        :return:
        """
        self.fake = Faker()
        self.regular_user = self.create_user_auth()
        self.staff_user = self.create_user_auth(username=self.staff_user_username, is_staff=True)
        name_surname = self.generate_name_and_surname(self.fake)
        self.regular_user_account = self.create_client_account(
            name=name_surname[0], surname=name_surname[1], user_account=self.regular_user
        )

        self.staff_user_account = self.create_client_account(
            name=name_surname[0], surname=name_surname[1], user_account=self.staff_user
        )

        super().setUp()

    def test_create_as_regular_user(self):
        name_surname = self.generate_name_and_surname(self.fake)
        user = self.create_user_auth(username=''.join(name_surname))
        self.assertTrue(
            self.client.login(username=user.username, password=self.default_user_password),
            msg='Login error'
        )
        payload = {
            "name": name_surname[0],
            "surname": name_surname[1]
        }
        self.set_url('api:client_api-list')
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(201, response.status_code)

        payload_unique_items = set(payload.items())
        response_json_unique_items = set(response.json().items())
        self.assertTrue(payload_unique_items.issubset(response_json_unique_items))

        self.assertTrue(ClientAccount.objects.get(user_account=user.id))
        self.client.logout()

    def test_create_a_regular_user_as_staff_user(self):
        name_surname = self.generate_name_and_surname(self.fake)
        user = self.create_user_auth(username=''.join(name_surname))
        staff = self.create_user_auth(
            username=''.join(self.generate_name_and_surname(self.fake)), is_staff=True
        )
        self.assertTrue(
            self.client.login(username=staff.username, password=self.default_user_password),
            msg='Login error'
        )
        payload = {
            "name": name_surname[0],
            "surname": name_surname[1],
            "user_account": user.id
        }
        self.set_url('api:client_api-list')
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(201, response.status_code)

        payload_unique_items = set(payload.items())
        response_json_unique_items = set(response.json().items())
        self.assertTrue(payload_unique_items.issubset(response_json_unique_items))

        self.client.logout()

    def test_partial_update(self):
        self.client.login(username=self.default_user_username, password=self.default_user_password)
        api_url_params = {
            "pk": self.regular_user_account.id
        }
        payload = {
            "city": self.fake.city(),
            "postal_code": self.fake.zipcode(),
        }
        self.set_url('api:client_api-detail', kwargs=api_url_params)
        response = self.client.patch(self.url, data=payload, format='json')
        self.assertEqual(200, response.status_code)

        payload_unique_items = set(payload.items())
        response_json_unique_items = set(response.json().items())
        self.assertTrue(payload_unique_items.issubset(response_json_unique_items))

        self.client.logout()

    def test_staff_updates_regular_user_account(self):
        self.client.login(username=self.staff_user_username, password=self.default_user_password)
        api_url_params = {
            "pk": self.regular_user_account.id
        }
        payload = {
            "city": self.fake.city(),
            "postal_code": self.fake.zipcode(),
        }
        self.set_url('api:client_api-detail', kwargs=api_url_params)
        response = self.client.patch(self.url, data=payload, format='json')
        self.assertEqual(200, response.status_code)

        payload_unique_items = set(payload.items())
        response_json_unique_items = set(response.json().items())
        self.assertTrue(payload_unique_items.issubset(response_json_unique_items))

        self.client.logout()

    def test_regular_user_can_not_update_staff_account(self):
        self.client.login(username=self.default_user_username, password=self.default_user_password)
        api_url_params = {
            "pk": self.staff_user_account.id
        }
        payload = {
            "city": self.fake.city(),
            "postal_code": self.fake.zipcode(),
        }
        self.set_url('api:client_api-detail', kwargs=api_url_params)
        response = self.client.patch(self.url, data=payload, format='json')
        self.assertEqual(404, response.status_code)
        self.client.logout()

    def test_regular_user_can_not_update_other_regular_user_account(self):
        name_surname = self.generate_name_and_surname(self.fake)
        user = self.create_user_auth(username=''.join(name_surname))
        user_account = self.create_client_account(
            name=name_surname[0], surname=name_surname[1], user_account=user
        )
        self.client.login(username=self.default_user_username, password=self.default_user_password)
        api_url_params = {
            "pk": user_account.id
        }
        payload = {
            "city": self.fake.city(),
            "postal_code": self.fake.zipcode(),
        }
        self.set_url('api:client_api-detail', kwargs=api_url_params)
        response = self.client.patch(self.url, data=payload, format='json')
        self.assertEqual(404, response.status_code)
        self.client.logout()

    def test_list_as_regular_user(self):
        self.client.login(username=self.default_user_username, password=self.default_user_password)
        self.set_url('api:client_api-list')
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.json()), 1)

    def test_list_as_staff_user(self):
        self.client.login(username=self.staff_user_username, password=self.default_user_password)
        self.set_url('api:client_api-list')
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.json()), 2)


class ClientWalletApiTests(CommonApiTests):
    fake = None
    api_reverse_url = 'api:client_wallet_api'
    regular_user = None
    staff_user = None
    regular_user_account = None
    staff_user_username = 'test_staff'
    staff_user_account = None

    def setUp(self):
        """
        Config

        * Docs
        ** Faker
        *** Examples: https://faker.readthedocs.io/en/stable/fakerclass.html#examples
        *** Unique values: https://faker.readthedocs.io/en/stable/fakerclass.html#unique-values
        :return:
        """
        self.fake = Faker()
        self.regular_user = self.create_user_auth()
        self.staff_user = self.create_user_auth(username=self.staff_user_username, is_staff=True)

        name_surname = self.generate_name_and_surname(self.fake)
        self.regular_user_account = self.create_client_account(
            name=name_surname[0], surname=name_surname[1], user_account=self.regular_user
        )
        self.staff_user_account = self.create_client_account(
            name=name_surname[0], surname=name_surname[1], user_account=self.staff_user
        )

        self.regular_user_wallet = self.create_client_wallet(self.regular_user_account)
        self.staff_user_wallet = self.create_client_wallet(self.staff_user_account)

        super().setUp()

    def test_create_regular_user_wallets_as_regular_user(self):
        self.assertTrue(
            self.client.login(
                username=self.default_user_username, password=self.default_user_password
            ),
            msg='Login error'
        )
        num_iterations = self.fake.pyint(min_value=2, max_value=10)
        for i in range(num_iterations):
            payload = {
                "client_account": self.regular_user_account.id
            }
            response_data = {
                "client_account": str(payload.get('client_account')),
            }
            self.set_url(f'{self.api_reverse_url}-list')
            response = self.client.post(self.url, data=payload, format='json')
            self.assertEqual(201, response.status_code)

        response_data_unique_items = set(response_data.items())
        response_json_unique_items = set(response.json().items())
        self.assertTrue(response_data_unique_items.issubset(response_json_unique_items))

        print(f'{num_iterations} wallets done')
        self.client.logout()

    def test_create_regular_user_wallets_as_other_user(self):
        """
        This wallet must return a 404, if not test fails
        """
        self.assertTrue(
            self.client.login(
                username=self.regular_user.username, password=self.default_user_password
            ),
            msg='Login error'
        )
        name_surname = self.generate_name_and_surname(self.fake)
        user = self.create_user_auth(username=''.join(name_surname))
        user_account = self.create_client_account(
            name=name_surname[0], surname=name_surname[1], user_account=user
        )

        payload = {
            "client_account": user_account.id
        }
        self.set_url(f'{self.api_reverse_url}-list')
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(404, response.status_code)
        self.client.logout()

    def test_create_regular_user_wallets_as_staff_user(self):
        self.assertTrue(
            self.client.login(
                username=self.staff_user_username, password=self.default_user_password
            ),
            msg='Login error'
        )
        num_iterations = self.fake.pyint(min_value=2, max_value=10)
        for i in range(num_iterations):
            payload = {
                "client_account": self.regular_user_account.id
            }
            response_data = {
                "client_account": str(payload.get('client_account')),
            }
            self.set_url(f'{self.api_reverse_url}-list')
            response = self.client.post(self.url, data=payload, format='json')
            self.assertEqual(201, response.status_code)

        response_data_unique_items = set(response_data.items())
        response_json_unique_items = set(response.json().items())
        self.assertTrue(response_data_unique_items.issubset(response_json_unique_items))

        print(f'{num_iterations} transactions done')
        self.client.logout()

    def test_create_staff_user_wallets_as_staff_user(self):
        self.assertTrue(
            self.client.login(
                username=self.staff_user_username, password=self.default_user_password
            ),
            msg='Login error'
        )
        name_surname = self.generate_name_and_surname(self.fake)
        user = self.create_user_auth(username=''.join(name_surname), is_staff=True)
        user_account = self.create_client_account(
            name=name_surname[0], surname=name_surname[1], user_account=user
        )

        num_iterations = self.fake.pyint(min_value=2, max_value=10)
        for i in range(num_iterations):
            payload = {
                "description": self.fake.pystr(),
                "amount": self.fake.pydecimal(left_digits=5, right_digits=2),
                "client_account": user_account.id
            }
            response_data = {
                "client_account": str(payload.get('client_account')),
            }
            self.set_url(f'{self.api_reverse_url}-list')
            response = self.client.post(self.url, data=payload, format='json')
            self.assertEqual(201, response.status_code)

        response_data_unique_items = set(response_data.items())
        response_json_unique_items = set(response.json().items())
        self.assertTrue(response_data_unique_items.issubset(response_json_unique_items))

        print(f'{num_iterations} transactions done')
        self.client.logout()

    def test_create_staff_user_wallets_as_regular_user(self):
        """
        This Wallet must return a 404, if not test fails
        """
        self.assertTrue(
            self.client.login(
                username=self.regular_user.username, password=self.default_user_password
            ),
            msg='Login error'
        )

        name_surname = self.generate_name_and_surname(self.fake)
        user = self.create_user_auth(username=''.join(name_surname), is_staff=True)
        user_account = self.create_client_account(
            name=name_surname[0], surname=name_surname[1], user_account=user
        )

        payload = {
            "client_account": user_account.id
        }
        self.set_url(f'{self.api_reverse_url}-list')
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(404, response.status_code)
        self.client.logout()

    def test_regular_user_wallets_list(self):
        self.assertTrue(
            self.client.login(
                username=self.default_user_username, password=self.default_user_password
            ),
            msg='Login error'
        )
        self.set_url(f'{self.api_reverse_url}-list')
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response.json()) > 0)

    def test_regular_user_wallet_retrieve(self):
        self.assertTrue(
            self.client.login(
                username=self.default_user_username, password=self.default_user_password
            ),
            msg='Login error'
        )
        self.set_url(f'{self.api_reverse_url}-detail', kwargs={"pk": self.regular_user_wallet.id})
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response.json()) > 0)

    def test_staff_user_wallets_list(self):
        self.assertTrue(
            self.client.login(
                username=self.staff_user_username, password=self.default_user_password
            ),
            msg='Login error'
        )
        self.set_url(f'{self.api_reverse_url}-list')
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response.json()) > 1)

    def test_staff_user_wallet_retrieve(self):
        self.assertTrue(
            self.client.login(
                username=self.staff_user_username, password=self.default_user_password
            ),
            msg='Login error'
        )
        self.set_url(f'{self.api_reverse_url}-detail', kwargs={"pk": self.staff_user_wallet.id})
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response.json()) > 0)

    def test_staff_user_retrieve_wallet_regular_user(self):
        self.assertTrue(
            self.client.login(
                username=self.staff_user_username, password=self.default_user_password
            ),
            msg='Login error'
        )
        self.set_url(f'{self.api_reverse_url}-detail', kwargs={"pk": self.regular_user_wallet.id})
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response.json()) > 0)


class ClientWalletTransactionApiTests(CommonApiTests, TransactionTestCase):
    fake = None
    regular_user = None
    staff_user = None
    regular_user_account = None
    staff_user_username = 'test_staff'
    staff_user_account = None
    regular_user_wallet = None
    staff_user_wallet = None
    regular_user_transaction = None
    staff_user_transaction = None

    def setUp(self):
        """
        Config

        * Docs
        ** Faker
        *** Examples: https://faker.readthedocs.io/en/stable/fakerclass.html#examples
        *** Unique values: https://faker.readthedocs.io/en/stable/fakerclass.html#unique-values
        :return:
        """
        self.fake = Faker()
        self.regular_user = self.create_user_auth()
        self.staff_user = self.create_user_auth(username=self.staff_user_username, is_staff=True)

        name_surname = self.generate_name_and_surname(self.fake)
        self.regular_user_account = self.create_client_account(
            name=name_surname[0], surname=name_surname[1], user_account=self.regular_user
        )
        self.staff_user_account = self.create_client_account(
            name=name_surname[0], surname=name_surname[1], user_account=self.staff_user
        )

        self.regular_user_wallet = self.create_client_wallet(self.regular_user_account)
        self.staff_user_wallet = self.create_client_wallet(self.staff_user_account)

        self.regular_user_transaction = self.create_client_transaction(
            self.fake.pydecimal(left_digits=5, right_digits=2), self.regular_user_wallet
        )

        self.staff_user_transaction = self.create_client_transaction(
            self.fake.pydecimal(left_digits=5, right_digits=2), self.staff_user_wallet
        )

        super().setUp()

    def test_create_regular_user_transactions_as_regular_user(self):
        self.assertTrue(
            self.client.login(
                username=self.default_user_username, password=self.default_user_password
            ),
            msg='Login error'
        )
        num_iterations = self.fake.pyint(min_value=2, max_value=10)
        for i in range(num_iterations):
            payload = {
                "description": self.fake.pystr(),
                "amount": self.fake.pydecimal(left_digits=5, right_digits=2),
                "client_wallet_account": self.regular_user_wallet.id
            }
            if payload.get('amount', 0) > 0:
                transaction_type = ClientWalletTransaction.Type.DEPOSIT.value
            elif payload.get('amount', 0) < 0:
                transaction_type = ClientWalletTransaction.Type.WITHDRAW.value
            else:
                transaction_type = ClientWalletTransaction.Type.TESTING.value
            response_data = {
                **payload,
                "amount": str(payload.get('amount')),
                "client_wallet_account": str(payload.get('client_wallet_account')),
                "transaction_type": transaction_type
            }
            self.set_url('api:client_wallet_transaction_api-list')
            response = self.client.post(self.url, data=payload, format='json')
            self.assertEqual(201, response.status_code)

        response_data_unique_items = set(response_data.items())
        response_json_unique_items = set(response.json().items())
        self.assertTrue(response_data_unique_items.issubset(response_json_unique_items))

        print(f'{num_iterations} transactions done')
        self.client.logout()

    def test_create_regular_user_transactions_as_other_user(self):
        """
        This transaction must return a 404, if not test fails
        """
        self.assertTrue(
            self.client.login(
                username=self.regular_user.username, password=self.default_user_password
            ),
            msg='Login error'
        )
        name_surname = self.generate_name_and_surname(self.fake)
        user = self.create_user_auth(username=''.join(name_surname))
        user_account = self.create_client_account(
            name=name_surname[0], surname=name_surname[1], user_account=user
        )
        user_wallet = self.create_client_wallet(user_account)

        payload = {
            "description": self.fake.pystr(),
            "amount": self.fake.pydecimal(left_digits=5, right_digits=2),
            "client_wallet_account": user_wallet.id
        }
        self.set_url('api:client_wallet_transaction_api-list')
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(404, response.status_code)
        self.client.logout()

    def test_create_regular_user_transactions_as_staff_user(self):
        self.assertTrue(
            self.client.login(
                username=self.staff_user_username, password=self.default_user_password
            ),
            msg='Login error'
        )
        num_iterations = self.fake.pyint(min_value=2, max_value=10)
        for i in range(num_iterations):
            payload = {
                "description": self.fake.pystr(),
                "amount": self.fake.pydecimal(left_digits=5, right_digits=2),
                "client_wallet_account": self.regular_user_wallet.id
            }
            if payload.get('amount', 0) > 0:
                transaction_type = ClientWalletTransaction.Type.DEPOSIT.value
            elif payload.get('amount', 0) < 0:
                transaction_type = ClientWalletTransaction.Type.WITHDRAW.value
            else:
                transaction_type = ClientWalletTransaction.Type.TESTING.value
            response_data = {
                **payload,
                "amount": str(payload.get('amount')),
                "client_wallet_account": str(payload.get('client_wallet_account')),
                "transaction_type": transaction_type
            }
            self.set_url('api:client_wallet_transaction_api-list')
            response = self.client.post(self.url, data=payload, format='json')
            self.assertEqual(201, response.status_code)

        response_data_unique_items = set(response_data.items())
        response_json_unique_items = set(response.json().items())
        self.assertTrue(response_data_unique_items.issubset(response_json_unique_items))

        print(f'{num_iterations} transactions done')
        self.client.logout()

    def test_create_staff_user_transactions_as_staff_user(self):
        self.assertTrue(
            self.client.login(
                username=self.staff_user_username, password=self.default_user_password
            ),
            msg='Login error'
        )
        name_surname = self.generate_name_and_surname(self.fake)
        user = self.create_user_auth(username=''.join(name_surname), is_staff=True)
        user_account = self.create_client_account(
            name=name_surname[0], surname=name_surname[1], user_account=user
        )
        user_wallet = self.create_client_wallet(user_account)

        num_iterations = self.fake.pyint(min_value=2, max_value=10)
        for i in range(num_iterations):
            payload = {
                "description": self.fake.pystr(),
                "amount": self.fake.pydecimal(left_digits=5, right_digits=2),
                "client_wallet_account": user_wallet.id
            }
            if payload.get('amount', 0) > 0:
                transaction_type = ClientWalletTransaction.Type.DEPOSIT.value
            elif payload.get('amount', 0) < 0:
                transaction_type = ClientWalletTransaction.Type.WITHDRAW.value
            else:
                transaction_type = ClientWalletTransaction.Type.TESTING.value
            response_data = {
                **payload,
                "amount": str(payload.get('amount')),
                "client_wallet_account": str(payload.get('client_wallet_account')),
                "transaction_type": transaction_type
            }
            self.set_url('api:client_wallet_transaction_api-list')
            response = self.client.post(self.url, data=payload, format='json')
            self.assertEqual(201, response.status_code)

        response_data_unique_items = set(response_data.items())
        response_json_unique_items = set(response.json().items())
        self.assertTrue(response_data_unique_items.issubset(response_json_unique_items))

        print(f'{num_iterations} transactions done')
        self.client.logout()

    def test_create_staff_user_transactions_as_regular_user(self):
        """
        This transaction must return a 404, if not test fails
        """
        self.assertTrue(
            self.client.login(
                username=self.regular_user.username, password=self.default_user_password
            ),
            msg='Login error'
        )

        name_surname = self.generate_name_and_surname(self.fake)
        user = self.create_user_auth(username=''.join(name_surname), is_staff=True)
        user_account = self.create_client_account(
            name=name_surname[0], surname=name_surname[1], user_account=user
        )
        user_wallet = self.create_client_wallet(user_account)

        payload = {
            "description": self.fake.pystr(),
            "amount": self.fake.pydecimal(left_digits=5, right_digits=2),
            "client_wallet_account": user_wallet.id
        }
        self.set_url('api:client_wallet_transaction_api-list')
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(404, response.status_code)
        self.client.logout()

    def test_regular_user_transaction_list(self):
        self.assertTrue(
            self.client.login(
                username=self.default_user_username, password=self.default_user_password
            ),
            msg='Login error'
        )
        self.set_url('api:client_wallet_transaction_api-list')
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response.json()) > 0)

    def test_regular_user_transaction_retrieve(self):
        self.assertTrue(
            self.client.login(
                username=self.default_user_username, password=self.default_user_password
            ),
            msg='Login error'
        )
        self.set_url('api:client_wallet_transaction_api-detail',
                     kwargs={"pk": self.regular_user_transaction.id})
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response.json()) > 0)

    def test_staff_user_transaction_list(self):
        self.assertTrue(
            self.client.login(
                username=self.staff_user_username, password=self.default_user_password
            ),
            msg='Login error'
        )
        self.set_url('api:client_wallet_transaction_api-list')
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response.json()) > 1)

    def test_staff_user_transaction_retrieve(self):
        self.assertTrue(
            self.client.login(
                username=self.staff_user_username, password=self.default_user_password
            ),
            msg='Login error'
        )
        self.set_url('api:client_wallet_transaction_api-detail',
                     kwargs={"pk": self.staff_user_transaction.id})
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response.json()) > 0)

    def test_staff_user_retrieve_transaction_regular_user(self):
        self.assertTrue(
            self.client.login(
                username=self.staff_user_username, password=self.default_user_password
            ),
            msg='Login error'
        )
        self.set_url('api:client_wallet_transaction_api-detail',
                     kwargs={"pk": self.regular_user_transaction.id})
        response = self.client.get(self.url, format='json')
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response.json()) > 0)
