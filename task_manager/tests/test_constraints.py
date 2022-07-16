"""Project constraints tests."""

from django.test import TestCase
from django.urls import reverse_lazy
from parameterized import parameterized_class

from labels.views import PROTECTED_ERROR_MESSAGE as LABELS_PROTECTED_ERROR_MESSAGE
from statuses.views import PROTECTED_ERROR_MESSAGE as STATUSES_PROTECTED_ERROR_MESSAGE
from task_manager.misc import get_response_messages, get_test_data
from tasks.views import PERMISSION_DENIED_MESSAGE as TASKS_PERMISSION_DENIED_MESSAGE
from users.views import LOGIN_REQUIRED_MESSAGE
from users.views import PERMISSION_DENIED_MESSAGE as USERS_PERMISSION_DENIED_MESSAGE
from users.views import PROTECTED_ERROR_MESSAGE as USERS_PROTECTED_ERROR_MESSAGE

test_data = get_test_data()

user = test_data['users']['existing']
another_user = test_data['users']['has_relationships']
status = test_data['statuses']['has_relationships']
label = test_data['labels']['has_relationships']
task = test_data['tasks']['existing']


@parameterized_class(
    ('url', 'id', 'message', 'redirect_url'),
    [
        (
            'users:update',
            another_user['pk'],
            USERS_PERMISSION_DENIED_MESSAGE,
            'users:index',
        ),
        (
            'users:delete',
            another_user['pk'],
            USERS_PERMISSION_DENIED_MESSAGE,
            'users:index',
        ),
        (
            'tasks:delete',
            task['pk'],
            TASKS_PERMISSION_DENIED_MESSAGE,
            'tasks:index',
        ),
    ],
)
class PermissionDeniedTest(TestCase):
    """Permission Denied tests."""

    fixtures = ['data.json']

    def test_permission_denied(self):
        self.client.login(
            username=user['username'],
            password=user['password'],
        )

        response = self.client.get(
            reverse_lazy(self.url, args=[self.id]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(self.message, response_messages)
        self.assertRedirects(response, reverse_lazy(self.redirect_url))


@parameterized_class(
    ('url', 'id'),
    [
        ('users:update', [user['pk']]),
        ('users:delete', [user['pk']]),
        ('statuses:index', None),
        ('statuses:create', None),
        ('statuses:update', [status['pk']]),
        ('statuses:delete', [status['pk']]),
        ('labels:index', None),
        ('labels:create', None),
        ('labels:update', [label['pk']]),
        ('labels:delete', [label['pk']]),
        ('tasks:index', None),
        ('tasks:create', None),
        ('tasks:update', [task['pk']]),
        ('tasks:delete', [task['pk']]),
    ],
)
class LoginRequiredTest(TestCase):
    """Login required tests."""

    fixtures = ['data.json']

    def test_login_required(self):
        response = self.client.get(reverse_lazy(self.url, args=self.id))
        response_messages = get_response_messages(response)

        self.assertIn(LOGIN_REQUIRED_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('login'))


@parameterized_class(
    ('url', 'id', 'message', 'redirect_url'),
    [
        (
            'users:delete',
            another_user['pk'],
            USERS_PROTECTED_ERROR_MESSAGE,
            'users:index',
        ),
        (
            'statuses:delete',
            status['pk'],
            STATUSES_PROTECTED_ERROR_MESSAGE,
            'statuses:index',
        ),
        (
            'labels:delete',
            label['pk'],
            LABELS_PROTECTED_ERROR_MESSAGE,
            'labels:index',
        ),
    ],
)
class ProtectedErrorTest(TestCase):
    """Protected error tests."""

    fixtures = ['data.json']

    def test_protected_error(self):
        self.client.login(
            username=another_user['username'],
            password=another_user['password'],
        )

        response = self.client.post(
            reverse_lazy(self.url, args=[self.id]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(self.message, response_messages)
        self.assertRedirects(response, reverse_lazy(self.redirect_url))
