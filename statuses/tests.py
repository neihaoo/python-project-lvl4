"""Statuses application tests."""

from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse_lazy
from parameterized import parameterized
from statuses import views
from statuses.models import Status
from task_manager.misc import get_response_messages, get_test_data


class StatusTest(TestCase):
    """Status views tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        status = test_data['statuses']['existing_status']

        cls.user = test_data['users']['existing_user']
        cls.status = Status.objects.get(name=status['name'])

    def setUp(self):
        self.client.login(
            username=self.user['username'],
            password=self.user['password'],
        )

    def test_index_page(self):
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
            views.IndexView.as_view().__name__,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_page(self):
        response = self.client.get(reverse_lazy('statuses:create'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'layouts/form.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.StatusCreationView.as_view().__name__,
        )

    def test_update_page(self):
        response = self.client.get(
            reverse_lazy('statuses:update', args=[self.status.pk]),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'layouts/form.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.StatusUpdateView.as_view().__name__,
        )

    def test_delete_page(self):
        response = self.client.get(
            reverse_lazy('statuses:delete', args=[self.status.pk]),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'delete.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.StatusDeleteView.as_view().__name__,
        )


class StatusCRUDTest(TestCase):
    """Status CRUD tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        status = test_data['statuses']['another_status']

        cls.status = Status.objects.get(name=status['name'])
        cls.new_status = test_data['statuses']['new_status']
        cls.user = test_data['users']['existing_user']

    def setUp(self):
        self.client.login(
            username=self.user['username'],
            password=self.user['password'],
        )

    def test_create(self):
        response = self.client.post(
            reverse_lazy('statuses:create'),
            self.new_status,
        )
        response_messages = get_response_messages(response)
        created_status = Status.objects.get(name=self.new_status['name'])

        self.assertIn(views.CREATION_SUCCESS_MESSAGE, response_messages)
        self.assertEqual(self.new_status['name'], created_status.name)
        self.assertRedirects(response, reverse_lazy('statuses:index'))

    def test_update(self):
        response = self.client.post(
            reverse_lazy('statuses:update', args=[self.status.pk]),
            self.new_status,
        )
        response_messages = get_response_messages(response)
        updated_status = Status.objects.get(pk=self.status.pk)

        self.assertIn(views.UPDATE_SUCCESS_MESSAGE, response_messages)
        self.assertEqual(self.new_status['name'], updated_status.name)
        self.assertRedirects(response, reverse_lazy('statuses:index'))

    def test_delete(self):
        response = self.client.post(
            reverse_lazy('statuses:delete', args=[self.status.pk]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(views.DELETE_SUCCESS_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('statuses:index'))

        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=self.status.pk)


class StatusPermissionTest(TestCase):
    """Status permissions tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        status = test_data['statuses']['existing_status']

        cls.status = Status.objects.get(name=status['name'])

    @parameterized.expand([('statuses:index',), ('statuses:create',)])
    def test_login_required(self, url):
        response = self.client.get(reverse_lazy(url))
        response_messages = get_response_messages(response)

        self.assertIn(views.LOGIN_REQUIRED_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('login'))

    @parameterized.expand([('statuses:update',), ('statuses:delete',)])
    def test_login_required_args(self, url):
        response = self.client.get(
            reverse_lazy(url, args=[self.status.pk]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(views.LOGIN_REQUIRED_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('login'))


class StatusErrorTest(TestCase):
    """Status errors tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        status = test_data['statuses']['existing_status']

        cls.status = Status.objects.get(name=status['name'])
        cls.user = test_data['users']['existing_user']

    def test_protected_error(self):
        self.client.login(
            username=self.user['username'],
            password=self.user['password'],
        )

        response = self.client.post(
            reverse_lazy('statuses:delete', args=[self.status.pk]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(views.PROTECTED_ERROR_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('statuses:index'))
