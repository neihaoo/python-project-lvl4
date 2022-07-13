"""Tasks application tests."""

from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse_lazy
from parameterized import parameterized
from task_manager.misc import get_response_messages, get_test_data
from tasks import views
from tasks.models import Task


class TaskTest(TestCase):
    """Task tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        task = test_data['tasks']['existing_task']

        cls.user = test_data['users']['existing_user']
        cls.task = Task.objects.get(name=task['name'])

    def setUp(self):
        self.client.login(
            username=self.user['username'],
            password=self.user['password'],
        )

    def test_index_page(self):
        tasks = Task.objects.all()
        response = self.client.get(reverse_lazy('tasks:index'))

        self.assertQuerysetEqual(
            response.context['task_list'],
            tasks,
            ordered=False,
        )
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.IndexView.as_view().__name__,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_page(self):
        response = self.client.get(reverse_lazy('tasks:create'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'layouts/form.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.TaskCreationView.as_view().__name__,
        )

    def test_update_page(self):
        response = self.client.get(
            reverse_lazy('tasks:update', args=[self.task.pk]),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'layouts/form.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.TaskUpdateView.as_view().__name__,
        )

    def test_delete_page(self):
        response = self.client.get(
            reverse_lazy('tasks:delete', args=[self.task.pk]),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'delete.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.TaskDeleteView.as_view().__name__,
        )


class TaskPermissionTest(TestCase):
    """Task permissions tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        task = test_data['tasks']['existing_task']

        cls.user = test_data['users']['another_user']
        cls.task = Task.objects.get(name=task['name'])

    def test_permission_denied(self):
        self.client.login(
            username=self.user['username'],
            password=self.user['password'],
        )

        response = self.client.get(
            reverse_lazy('tasks:delete', args=[self.task.pk]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(views.PERMISSION_DENIED_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('tasks:index'))

    @parameterized.expand([('tasks:index',), ('tasks:create',)])
    def test_login_required(self, url):
        response = self.client.get(reverse_lazy(url))
        response_messages = get_response_messages(response)

        self.assertIn(views.LOGIN_REQUIRED_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('login'))

    @parameterized.expand([('tasks:update',), ('tasks:delete',)])
    def test_login_required_args(self, url):
        response = self.client.get(
            reverse_lazy(url, args=[self.task.pk]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(views.LOGIN_REQUIRED_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('login'))


class TaskCRUDTest(TestCase):
    """Task CRUD tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        task = test_data['tasks']['another_task']

        cls.task = Task.objects.get(name=task['name'])
        cls.new_task = test_data['tasks']['new_task']
        cls.user = test_data['users']['task_user']

    def setUp(self):
        self.client.login(
            username=self.user['username'],
            password=self.user['password'],
        )

    def test_create(self):
        response = self.client.post(
            reverse_lazy('tasks:create'),
            self.new_task,
        )
        response_messages = get_response_messages(response)
        created_task = Task.objects.get(name=self.new_task['name'])

        self.assertIn(views.CREATION_SUCCESS_MESSAGE, response_messages)
        self.assertEqual(self.new_task['name'], created_task.name)
        self.assertRedirects(response, reverse_lazy('tasks:index'))

    def test_update(self):
        response = self.client.post(
            reverse_lazy('tasks:update', args=[self.task.pk]),
            self.new_task,
        )
        response_messages = get_response_messages(response)
        updated_task = Task.objects.get(pk=self.task.pk)

        self.assertIn(views.UPDATE_SUCCESS_MESSAGE, response_messages)
        self.assertEqual(self.new_task['name'], updated_task.name)
        self.assertRedirects(response, reverse_lazy('tasks:index'))

    def test_delete(self):
        response = self.client.post(
            reverse_lazy('tasks:delete', args=[self.task.pk]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(views.DELETE_SUCCESS_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('tasks:index'))

        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=self.task.pk)
