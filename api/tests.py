from django.contrib.auth.models import User
from django.test import TransactionTestCase
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.models import ClientAccount, ClientWallet

from faker import Faker


# api.tests.ClientAccountApiTests.test_create_regular_user_and_sign_in
class CommonApiTests(APITestCase):
    default_user_username = 'testuser'
    default_user_password = 'aaa'

    def normalize_username(self, text=''):
        return text.lower().replace(' ', '_')

    def create_user_auth(self, username=default_user_username,
                         password=default_user_password, is_staff=False):
        user, is_created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.is_staff = is_staff
        user.is_active = True
        user.is_superuser = False
        user.save()
        return user

        # group, is_created = Group.objects.get_or_create(name='testgroup')
        # user.groups.add(group)
        # for perm in Permission.objects.all():
        #     group.permissions.add(perm)

    def create_client_account(self, name='', surname='', user_account=None):
        return ClientAccount.objects.create(name=name, surname=surname, user_account=user_account)

    # def create_user_auth(cls):
    #     user, is_created = User.objects.get_or_create(username='testuser')
    #     user.set_password('aaa')
    #     user.is_staff = True
    #     user.is_active = True
    #     user.is_superuser = True
    #     user.save()
    #
    #     group, is_created = Group.objects.get_or_create(name='testgroup')
    #     user.groups.add(group)
    #     for perm in Permission.objects.all():
    #         group.permissions.add(perm)

    def set_url(self, name, kwargs=None):
        self.url = reverse(name, kwargs=kwargs)
        self.full_url = 'http://testserver' + self.url


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
        self.assertDictContainsSubset(response_data, response.json())
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
        self.assertDictContainsSubset(response_data, response.json())
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
        self.assertDictContainsSubset(response_data, response.json())

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
        self.assertDictContainsSubset(response_data, response.json())


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
        name_surname = self.__generate_name_and_surname()
        self.regular_user_account = ClientAccount.objects.create(
            name=name_surname[0], surname=name_surname[1], user_account=self.regular_user
        )

        self.staff_user_account = ClientAccount.objects.create(
            name=name_surname[0], surname=name_surname[1], user_account=self.staff_user
        )

        super().setUp()

    def __generate_name_and_surname(self):
        name = self.normalize_username(self.fake.unique.first_name())
        surname = self.normalize_username(self.fake.unique.last_name())
        return [name, surname]

    def test_create_as_regular_user(self):
        name_surname = self.__generate_name_and_surname()
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
        self.assertDictContainsSubset(payload, response.json())
        self.assertTrue(ClientAccount.objects.get(user_account=user.id))
        self.client.logout()

    def test_create_a_regular_user_as_staff_user(self):
        name_surname = self.__generate_name_and_surname()
        user = self.create_user_auth(username=''.join(name_surname))
        staff = self.create_user_auth(
            username=''.join(self.__generate_name_and_surname()), is_staff=True
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
        self.assertDictContainsSubset(payload, response.json())
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
        self.assertDictContainsSubset(payload, response.json())
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
        self.assertDictContainsSubset(payload, response.json())
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
        name_surname = self.__generate_name_and_surname()
        user = self.create_user_auth(username=''.join(name_surname))
        user_account = ClientAccount.objects.create(
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
