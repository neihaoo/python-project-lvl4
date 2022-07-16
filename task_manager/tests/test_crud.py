"""Project CRUD tests."""

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse_lazy
from parameterized import parameterized_class

from labels.models import Label
from labels.views import CREATION_SUCCESS_MESSAGE as LABEL_CREATION_SUCCESS_MESSAGE
from labels.views import DELETE_SUCCESS_MESSAGE as LABEL_DELETE_SUCCESS_MESSAGE
from labels.views import UPDATE_SUCCESS_MESSAGE as LABEL_UPDATE_SUCCESS_MESSAGE
from statuses.models import Status
from statuses.views import CREATION_SUCCESS_MESSAGE as STATUS_CREATION_SUCCESS_MESSAGE
from statuses.views import DELETE_SUCCESS_MESSAGE as STATUS_DELETE_SUCCESS_MESSAGE
from statuses.views import UPDATE_SUCCESS_MESSAGE as STATUS_UPDATE_SUCCESS_MESSAGE
from task_manager.misc import get_response_messages, get_test_data
from tasks.models import Task
from tasks.views import CREATION_SUCCESS_MESSAGE as TASK_CREATION_SUCCESS_MESSAGE
from tasks.views import DELETE_SUCCESS_MESSAGE as TASK_DELETE_SUCCESS_MESSAGE
from tasks.views import UPDATE_SUCCESS_MESSAGE as TASK_UPDATE_SUCCESS_MESSAGE
from users.models import User
from users.views import CREATION_SUCCESS_MESSAGE as USER_CREATION_SUCCESS_MESSAGE
from users.views import DELETE_SUCCESS_MESSAGE as USER_DELETE_SUCCESS_MESSAGE
from users.views import UPDATE_SUCCESS_MESSAGE as USER_UPDATE_SUCCESS_MESSAGE

test_data = get_test_data()

user = test_data['users']['existing']
new_user = test_data['users']['new']
task_owner = test_data['users']['has_relationships']

status = test_data['statuses']['existing']
new_status = test_data['statuses']['new']

label = test_data['labels']['existing']
new_label = test_data['labels']['new']

task = test_data['tasks']['existing']
new_task = test_data['tasks']['new']


class CreateUserTest(TestCase):
    """Create user test."""

    fixtures = ['data.json']

    def test_create_user(self):
        response = self.client.post(reverse_lazy('users:create'), new_user)
        response_messages = get_response_messages(response)
        created_user = User.objects.get(username=new_user['username'])

        self.assertIn(USER_CREATION_SUCCESS_MESSAGE, response_messages)
        self.assertEqual(new_user['username'], created_user.username)
        self.assertRedirects(response, reverse_lazy('login'))


@parameterized_class(
    ('url', 'new_data', 'model', 'message', 'redirect_url'),
    [
        (
            'statuses:create',
            new_status,
            Status,
            STATUS_CREATION_SUCCESS_MESSAGE,
            'statuses:index',
        ),
        (
            'labels:create',
            new_label,
            Label,
            LABEL_CREATION_SUCCESS_MESSAGE,
            'labels:index',
        ),
        (
            'tasks:create',
            new_task,
            Task,
            TASK_CREATION_SUCCESS_MESSAGE,
            'tasks:index',
        ),
    ],
)
class CreateTest(TestCase):
    """Create test."""

    fixtures = ['data.json']

    def test_create(self):
        self.client.login(
            username=user['username'],
            password=user['password'],
        )

        response = self.client.post(reverse_lazy(self.url), self.new_data)
        response_messages = get_response_messages(response)
        created_data = self.model.objects.get(name=self.new_data['name'])

        self.assertIn(self.message, response_messages)
        self.assertEqual(self.new_data['name'], created_data.name)
        self.assertRedirects(response, reverse_lazy(self.redirect_url))


class UpdateUserTest(TestCase):
    """Update user test."""

    fixtures = ['data.json']

    def test_update_user(self):
        self.client.login(
            username=user['username'],
            password=user['password'],
        )

        response = self.client.post(
            reverse_lazy('users:update', args=[user['pk']]),
            new_user,
        )
        response_messages = get_response_messages(response)
        updated_user = User.objects.get(username=new_user['username'])

        self.assertIn(USER_UPDATE_SUCCESS_MESSAGE, response_messages)
        self.assertEqual(new_user['username'], updated_user.username)
        self.assertRedirects(response, reverse_lazy('users:index'))


@parameterized_class(
    (
        'url',
        'id',
        'new_data',
        'model',
        'message',
        'redirect_url',
    ),
    [
        (
            'statuses:update',
            status['pk'],
            new_status,
            Status,
            STATUS_UPDATE_SUCCESS_MESSAGE,
            'statuses:index',
        ),
        (
            'labels:update',
            label['pk'],
            new_label,
            Label,
            LABEL_UPDATE_SUCCESS_MESSAGE,
            'labels:index',
        ),
        (
            'tasks:update',
            task['pk'],
            new_task,
            Task,
            TASK_UPDATE_SUCCESS_MESSAGE,
            'tasks:index',
        ),
    ],
)
class UpdateTest(TestCase):
    """Update test."""

    fixtures = ['data.json']

    def test_update(self):
        self.client.login(
            username=user['username'],
            password=user['password'],
        )

        response = self.client.post(
            reverse_lazy(self.url, args=[self.id]),
            self.new_data,
        )
        response_messages = get_response_messages(response)
        updated_data = self.model.objects.get(name=self.new_data['name'])

        self.assertIn(self.message, response_messages)
        self.assertEqual(self.new_data['name'], updated_data.name)
        self.assertRedirects(response, reverse_lazy(self.redirect_url))


class DeleteUserTest(TestCase):
    """Delete user tests."""

    fixtures = ['data.json']

    def test_delete_user(self):
        self.client.login(
            username=user['username'],
            password=user['password'],
        )

        response = self.client.post(
            reverse_lazy('users:delete', args=[user['pk']]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(USER_DELETE_SUCCESS_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('users:index'))

        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=user['pk'])


@parameterized_class(
    (
        'url',
        'id',
        'message',
        'redirect_url',
        'model',
    ),
    [
        (
            'statuses:delete',
            status['pk'],
            STATUS_DELETE_SUCCESS_MESSAGE,
            'statuses:index',
            Status,
        ),
        (
            'labels:delete',
            label['pk'],
            LABEL_DELETE_SUCCESS_MESSAGE,
            'labels:index',
            Label,
        ),
        (
            'tasks:delete',
            task['pk'],
            TASK_DELETE_SUCCESS_MESSAGE,
            'tasks:index',
            Task,
        ),
    ],
)
class DeleteTest(TestCase):
    """Delete tests."""

    fixtures = ['data.json']

    def test_delete(self):
        self.client.login(
            username=task_owner['username'],
            password=task_owner['password'],
        )

        response = self.client.post(
            reverse_lazy(self.url, args=[self.id]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(self.message, response_messages)
        self.assertRedirects(response, reverse_lazy(self.redirect_url))

        with self.assertRaises(ObjectDoesNotExist):
            self.model.objects.get(pk=self.id)
