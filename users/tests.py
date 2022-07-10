"""Application tests."""

from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse_lazy
from task_manager.misc import get_test_data
from users.views import IndexView, user_messages


class UserTest(TestCase):
    """User tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        cls.new_user = test_data['users']['new_user']
        cls.existing_user = test_data['users']['existing_user']
        cls.model = get_user_model()

    def test_index_page(self):
        users = self.model.objects.all()
        response = self.client.get(reverse_lazy('users:index'))

        self.assertQuerysetEqual(
            response.context['user_list'],
            users,
            ordered=False,
        )
        self.assertTemplateUsed(response, 'users/user_list.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            IndexView.as_view().__name__,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create(self):
        response = self.client.post(
            reverse_lazy('users:create'),
            {
                'username': self.new_user['username'],
                'password1': self.new_user['password'],
                'password2': self.new_user['password'],
            },
        )
        response_messages = [
            messages.message
            for messages in get_messages(response.wsgi_request)
        ]
        created_user = self.model.objects.get(
            username=self.new_user['username'],
        )

        self.assertIn(user_messages['creation_success'], response_messages)
        self.assertEqual(self.new_user['username'], created_user.username)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_update(self):
        user = self.model.objects.get(username=self.existing_user['username'])

        self.client.force_login(user)

        response = self.client.post(
            reverse_lazy('users:update', args=[user.pk]),
            {
                'username': self.new_user['username'],
                'password1': self.new_user['password'],
                'password2': self.new_user['password'],
            },
        )
        response_messages = [
            messages.message
            for messages in get_messages(response.wsgi_request)
        ]
        updated_user = self.model.objects.get(pk=user.pk)

        self.assertIn(user_messages['update_success'], response_messages)
        self.assertEqual(self.new_user['username'], updated_user.username)
        self.assertRedirects(response, reverse_lazy('users:index'))

    def test_delete(self):
        user = self.model.objects.get(username=self.existing_user['username'])

        self.client.force_login(user)

        response = self.client.post(
            reverse_lazy('users:delete', args=[user.pk]),
        )
        response_messages = [
            messages.message
            for messages in get_messages(response.wsgi_request)
        ]

        self.assertIn(user_messages['delete_success'], response_messages)
        self.assertRedirects(response, reverse_lazy('users:index'))

        with self.assertRaises(ObjectDoesNotExist):
            self.model.objects.get(pk=user.pk)
