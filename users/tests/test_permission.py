"""Users permission tests."""

import json
import os

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy
from parameterized import parameterized_class
from users.mixins import permission_messages
from users.models import User

DIR_PATH = os.path.dirname(__file__)


def get_fixture_path(filename):
    return os.path.join(DIR_PATH, 'fixtures', filename)


def read_file(filename):
    with open(get_fixture_path(filename)) as data_file:
        return data_file.read()


def get_test_data():
    return json.loads(read_file('test_data.json'))


@parameterized_class('url', [('users:update',), ('users:delete',)])
class UserPermissionTest(TestCase):
    """Test users permission."""

    fixtures = ['users/tests/fixtures/users.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        cls.existing_user = test_data['users']['existing_user']
        cls.another_user = test_data['users']['another_user']

    def test_auth_permission(self):
        user = User.objects.get(username=self.existing_user['username'])
        response = self.client.get(reverse_lazy(self.url, args=[user.pk]))
        response_messages = [
            messages.message
            for messages in get_messages(response.wsgi_request)
        ]

        self.assertIn(permission_messages['login_required'], response_messages)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_permission(self):
        user = User.objects.get(username=self.existing_user['username'])
        checked_user = User.objects.get(username=self.another_user['username'])

        self.client.force_login(checked_user)

        response = self.client.get(reverse_lazy(self.url, args=[user.pk]))
        response_messages = [
            messages.message
            for messages in get_messages(response.wsgi_request)
        ]

        self.assertIn(
            permission_messages['permission_denied'],
            response_messages,
        )
        self.assertRedirects(response, reverse_lazy('users:index'))
