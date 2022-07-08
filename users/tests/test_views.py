"""Users views tests."""

import json
import os
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy
from users.models import User
from users.views import (
    IndexView,
    UserCreationView,
    UserDeleteView,
    UserLoginView,
    UserUpdateView,
)

DIR_PATH = os.path.dirname(__file__)


def get_fixture_path(filename):
    return os.path.join(DIR_PATH, 'fixtures', filename)


def read_file(filename):
    with open(get_fixture_path(filename)) as data_file:
        return data_file.read()


def get_test_data():
    return json.loads(read_file('test_data.json'))


class UsersViewsTest(TestCase):
    """Test users views."""

    fixtures = ['users/tests/fixtures/users.json']

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data()

    def test_index_page(self):
        users = User.objects.all()
        response = self.client.get(reverse_lazy('users:index'))

        self.assertQuerysetEqual(
            response.context['user_list'],
            users,
            ordered=False,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/index.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            IndexView.as_view().__name__,
        )

    def test_create_user_page(self):
        response = self.client.get(reverse_lazy('users:create'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/create.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            UserCreationView.as_view().__name__,
        )

    def test_update_user_page(self):
        existing_user = self.test_data['users']['existing_user']
        user = User.objects.get(username=existing_user['username'])

        self.client.force_login(user)

        response = self.client.get(
            reverse_lazy('users:update', args=[user.pk]),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/update.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            UserUpdateView.as_view().__name__,
        )

    def test_delete_user_page(self):
        existing_user = self.test_data['users']['existing_user']
        user = User.objects.get(username=existing_user['username'])

        self.client.force_login(user)

        response = self.client.get(
            reverse_lazy('users:delete', args=[user.pk]),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/delete.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            UserDeleteView.as_view().__name__,
        )

    def test_login_page(self):
        response = self.client.get(reverse_lazy('login'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            UserLoginView.as_view().__name__,
        )
