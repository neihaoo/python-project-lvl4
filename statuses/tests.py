"""Application tests."""

from http import HTTPStatus

from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse_lazy
from statuses.models import Status
from statuses.views import IndexView, status_messages
from task_manager.misc import get_test_data


class StatusTest(TestCase):
    """Status tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        cls.new_status = test_data['statuses']['new_status']
        cls.existing_status = test_data['statuses']['existing_status']
        cls.existing_user = test_data['users']['existing_user']

    def test_index_page(self):
        self.client.login(
            username=self.existing_user['username'],
            password=self.existing_user['password'],
        )

        statuses = Status.objects.all()
        response = self.client.get(reverse_lazy('statuses:index'))

        self.assertQuerysetEqual(
            response.context['status_list'],
            statuses,
            ordered=False,
        )
        self.assertTemplateUsed(response, 'statuses/status_list.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            IndexView.as_view().__name__,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create(self):
        self.client.login(
            username=self.existing_user['username'],
            password=self.existing_user['password'],
        )

        response = self.client.post(
            reverse_lazy('statuses:create'),
            self.new_status,
        )
        response_messages = [
            messages.message
            for messages in get_messages(response.wsgi_request)
        ]
        created_status = Status.objects.get(name=self.new_status['name'])

        self.assertIn(status_messages['creation_success'], response_messages)
        self.assertEqual(self.new_status['name'], created_status.name)
        self.assertRedirects(response, reverse_lazy('statuses:index'))

    def test_update(self):
        self.client.login(
            username=self.existing_user['username'],
            password=self.existing_user['password'],
        )

        status = Status.objects.get(name=self.existing_status['name'])
        response = self.client.post(
            reverse_lazy('statuses:update', args=[status.pk]),
            self.new_status,
        )
        response_messages = [
            messages.message
            for messages in get_messages(response.wsgi_request)
        ]
        updated_status = Status.objects.get(pk=status.pk)

        self.assertIn(status_messages['update_success'], response_messages)
        self.assertEqual(self.new_status['name'], updated_status.name)
        self.assertRedirects(response, reverse_lazy('statuses:index'))

    def test_delete(self):
        self.client.login(
            username=self.existing_user['username'],
            password=self.existing_user['password'],
        )

        status = Status.objects.get(name=self.existing_status['name'])
        response = self.client.post(
            reverse_lazy('statuses:delete', args=[status.pk]),
        )
        response_messages = [
            messages.message
            for messages in get_messages(response.wsgi_request)
        ]

        self.assertIn(status_messages['delete_success'], response_messages)
        self.assertRedirects(response, reverse_lazy('statuses:index'))

        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=status.pk)
