"""Users auth tests."""

import json
import os

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy
from users.views import users_messages

DIR_PATH = os.path.dirname(__file__)


def get_fixture_path(filename):
    return os.path.join(DIR_PATH, 'fixtures', filename)


def read_file(filename):
    with open(get_fixture_path(filename)) as data_file:
        return data_file.read()


def get_test_data():
    return json.loads(read_file('test_data.json'))


class UserAuthTest(TestCase):
    """Test user login and logout."""

    fixtures = ['users/tests/fixtures/users.json']

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data()

    def test_login_message(self):
        user = self.test_data['users']['existing_user']
        response = self.client.post(
            reverse_lazy('login'),
            {'username': user['username'], 'password': user['password']},
        )
        response_messages = [
            messages.message
            for messages in get_messages(response.wsgi_request)
        ]

        self.assertIn(users_messages['login_success'], response_messages)
        self.assertRedirects(response, reverse_lazy('index'))

    def test_logout_message(self):
        user = self.test_data['users']['existing_user']
        self.client.post(
            reverse_lazy('login'),
            {'username': user['username'], 'password': user['password']},
        )

        response = self.client.post(reverse_lazy('logout'))
        response_messages = [
            messages.message
            for messages in get_messages(response.wsgi_request)
        ]

        self.assertIn(users_messages['logout_success'], response_messages)
        self.assertRedirects(response, reverse_lazy('index'))
