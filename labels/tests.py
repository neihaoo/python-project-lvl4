"""labels application tests."""

from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse_lazy
from labels import views
from labels.models import Label
from parameterized import parameterized
from task_manager.misc import get_response_messages, get_test_data


class LabelTest(TestCase):
    """Label views tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        label = test_data['labels']['existing_label']

        cls.user = test_data['users']['existing_user']
        cls.label = Label.objects.get(name=label['name'])

    def setUp(self):
        self.client.login(
            username=self.user['username'],
            password=self.user['password'],
        )

    def test_index_page(self):
        labels = Label.objects.all()
        response = self.client.get(reverse_lazy('labels:index'))

        self.assertQuerysetEqual(
            response.context['label_list'],
            labels,
            ordered=False,
        )
        self.assertTemplateUsed(response, 'labels/label_list.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.IndexView.as_view().__name__,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_page(self):
        response = self.client.get(reverse_lazy('labels:create'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'layouts/form.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.LabelCreationView.as_view().__name__,
        )

    def test_update_page(self):
        response = self.client.get(
            reverse_lazy('labels:update', args=[self.label.pk]),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'layouts/form.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.LabelUpdateView.as_view().__name__,
        )

    def test_delete_page(self):
        response = self.client.get(
            reverse_lazy('labels:delete', args=[self.label.pk]),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'delete.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.LabelDeleteView.as_view().__name__,
        )


class LabelCRUDTest(TestCase):
    """Label CRUD tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        label = test_data['labels']['another_label']

        cls.label = Label.objects.get(name=label['name'])
        cls.new_label = test_data['labels']['new_label']
        cls.user = test_data['users']['existing_user']

    def setUp(self):
        self.client.login(
            username=self.user['username'],
            password=self.user['password'],
        )

    def test_create(self):
        response = self.client.post(
            reverse_lazy('labels:create'),
            self.new_label,
        )
        response_messages = get_response_messages(response)
        created_status = Label.objects.get(name=self.new_label['name'])

        self.assertIn(views.CREATION_SUCCESS_MESSAGE, response_messages)
        self.assertEqual(self.new_label['name'], created_status.name)
        self.assertRedirects(response, reverse_lazy('labels:index'))

    def test_update(self):
        response = self.client.post(
            reverse_lazy('labels:update', args=[self.label.pk]),
            self.new_label,
        )
        response_messages = get_response_messages(response)
        updated_status = Label.objects.get(pk=self.label.pk)

        self.assertIn(views.UPDATE_SUCCESS_MESSAGE, response_messages)
        self.assertEqual(self.new_label['name'], updated_status.name)
        self.assertRedirects(response, reverse_lazy('labels:index'))

    def test_delete(self):
        response = self.client.post(
            reverse_lazy('labels:delete', args=[self.label.pk]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(views.DELETE_SUCCESS_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('labels:index'))

        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(pk=self.label.pk)


class LabelPermissionTest(TestCase):
    """Label permissions tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        label = test_data['labels']['existing_label']

        cls.label = Label.objects.get(name=label['name'])

    @parameterized.expand([('labels:index',), ('labels:create',)])
    def test_login_required(self, url):
        response = self.client.get(reverse_lazy(url))
        response_messages = get_response_messages(response)

        self.assertIn(views.LOGIN_REQUIRED_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('login'))

    @parameterized.expand([('labels:update',), ('labels:delete',)])
    def test_login_required_args(self, url):
        response = self.client.get(
            reverse_lazy(url, args=[self.label.pk]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(views.LOGIN_REQUIRED_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('login'))


class LabelErrorTest(TestCase):
    """Label errors tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        label = test_data['labels']['existing_label']

        cls.label = Label.objects.get(name=label['name'])
        cls.user = test_data['users']['existing_user']

    def test_protected_error(self):
        self.client.login(
            username=self.user['username'],
            password=self.user['password'],
        )

        response = self.client.post(
            reverse_lazy('labels:delete', args=[self.label.pk]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(views.PROTECTED_ERROR_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('labels:index'))
