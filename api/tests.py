from django.contrib.auth.models import User
from django.test import TestCase
from django.test import tag
from requests.auth import HTTPBasicAuth
from rest_framework.reverse import reverse
from rest_framework.test import RequestsClient

from api.models import ClientAccount
from api.test_extras.test_globals import *

"""
This tests was made to test Rest API behavior

Author: Adrian G
Created: 2019/03/16
Contact:  mroot5@outlook.es
Notes:
test --keepdb
https://docs.djangoproject.com/en/dev/ref/django-admin/#cmdoption-test-keepdb

test --failfast
https://docs.djangoproject.com/en/dev/ref/django-admin/#cmdoption-test-failfast

assertRaise: capture an exception.
If an exception is reaised the test is ok on the other hand the test fail

https://docs.djangoproject.com/en/dev/topics/testing/tools/#exceptions
https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaises

Terminal colors:
* Yellow: \e[33mText\e[0m
* Red: \e[32mText\e[0m
"""


class ExampleTests(TestCase):
    def setUp(self):
        self.num0 = '2'
        self.num1 = 2

    @tag("no-test")
    def test_check_if_exception_is_raised(self):
        """
        This test will be ok because we capture the TypeError
        as we want
        """
        with self.assertRaises(TypeError):
            sum = self.num0 + self.num1

    @tag("no-test")
    def test_exception_is_raised_without_chek(self):
        """
        This test must fail because an exception is raised.
        Skipped, this test is for documentation.
        """
        sum = self.num0 + self.num1


class UserApiTests(TestCase):

    def setUp(self):
        self.request_client = RequestsClient()
        self.user_pk = 0

    def test_create_user_with_api(self):
        api_data = {
            "username": DEFAULT_CLIENT_USERNAME,
            "password": DEFAULT_CLIENT_PASSWORD,
            "email": DEFAULT_CLIENT_EMAIL,
        }
        api_url = reverse('api:user_api-list')
        response = self.request_client.post(TEST_URL + api_url, data=api_data)
        self.assertEqual(201, response.status_code)


class ClienAccountModelTests(TestCase):
    def setUp(self):
        self.request_client = RequestsClient()
        self.user = User.objects.create_user(username=DEFAULT_CLIENT_USERNAME, password=DEFAULT_CLIENT_PASSWORD)
        self.client_name = "John"
        self.client_surname = "Doe"

    def test_client_create(self):
        api_data = {
            "name": self.client_name,
            "surname": self.client_surname,
            "user_account": self.user.pk,
        }
        api_url = reverse('api:client_api-list')
        self.request_client.auth = HTTPBasicAuth(DEFAULT_CLIENT_USERNAME, DEFAULT_CLIENT_PASSWORD)
        response = self.request_client.post(TEST_URL + api_url, data=api_data)
        self.assertEqual(201, response.status_code)

    def test_client_full_update(self):
        client = ClientAccount.objects.create(name=self.client_name, surname=self.client_surname, user_account=self.user)
        api_url_params = {
            "pk": client.id
        }
        api_data = {
            "name": self.client_name,
            "surname": self.client_surname,
            "city": "Madrid",
            "user_account": self.user.pk,
        }
        api_url = reverse('api:client_api-detail', kwargs=api_url_params)
        self.request_client.auth = HTTPBasicAuth(DEFAULT_CLIENT_USERNAME, DEFAULT_CLIENT_PASSWORD)
        response = self.request_client.patch(TEST_URL + api_url, data=api_data)
        self.assertEqual(200, response.status_code)

    def test_client_partial_update(self):
        client = ClientAccount.objects.create(name=self.client_name, surname=self.client_surname, user_account=self.user)
        api_url_params = {
            "pk": client.id
        }
        api_data = {
            "city": "Madrid",
            "postal_code": "28000",
        }
        api_url = reverse('api:client_api-detail', kwargs=api_url_params)
        self.request_client.auth = HTTPBasicAuth(DEFAULT_CLIENT_USERNAME, DEFAULT_CLIENT_PASSWORD)
        response = self.request_client.patch(TEST_URL + api_url, data=api_data)
        self.assertEqual(200, response.status_code)
