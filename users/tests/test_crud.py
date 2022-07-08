"""Users CRUD tests."""

import json
import os

from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse_lazy
from users.models import User
from users.views import users_messages

DIR_PATH = os.path.dirname(__file__)


def get_fixture_path(filename):
    return os.path.join(DIR_PATH, 'fixtures', filename)


def read_file(filename):
    with open(get_fixture_path(filename)) as data_file:
        return data_file.read()


def get_test_data():
    return json.loads(read_file('test_data.json'))


class UserCRUDTest(TestCase):
    """Test users CRUD."""

    fixtures = ['users/tests/fixtures/users.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        cls.new_user = test_data['users']['new_user']
        cls.existing_user = test_data['users']['existing_user']

    def test_create_user(self):
        response = self.client.post(
            reverse_lazy('users:create'),
            self.new_user,
        )
        response_messages = [
            messages.message
            for messages in get_messages(response.wsgi_request)
        ]
        created_user = User.objects.get(username=self.new_user['username'])

        self.assertIn(users_messages['creation_success'], response_messages)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertEqual(self.new_user['username'], created_user.username)

    def test_update_user(self):
        user = User.objects.get(username=self.existing_user['username'])

        self.client.force_login(user)

        response = self.client.post(
            reverse_lazy('users:update', args=[user.pk]),
            self.new_user,
        )
        response_messages = [
            messages.message
            for messages in get_messages(response.wsgi_request)
        ]
        updated_user = User.objects.get(pk=user.pk)

        self.assertIn(users_messages['update_success'], response_messages)
        self.assertRedirects(response, reverse_lazy('users:index'))
        self.assertEqual(self.new_user['username'], updated_user.username)

    def test_delete_user(self):
        user = User.objects.get(username=self.existing_user['username'])

        self.client.force_login(user)

        response = self.client.post(
            reverse_lazy('users:delete', args=[user.pk]),
        )
        response_messages = [
            messages.message
            for messages in get_messages(response.wsgi_request)
        ]

        self.assertIn(users_messages['delete_success'], response_messages)
        self.assertRedirects(response, reverse_lazy('users:index'))
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=user.pk)
