from django.test import TestCase, tag

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


@tag("no-test")
class SampleTests(TestCase):
    def setUp(self):
        self.num0 = '2'
        self.num1 = 2

    @tag("no-test")
    def __test_check_if_exception_is_raised(self):
        """
        This test will be ok because we capture the TypeError
        as we want
        """
        with self.assertRaises(TypeError):
            sum = self.num0 + self.num1

    @tag("no-test")
    def __test_exception_is_raised_without_chek(self):
        """
        This test must fail because an exception is raised.
        Skipped, this test is for documentation.
        """
        sum = self.num0 + self.num1
