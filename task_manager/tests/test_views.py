"""Project view tests."""

from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy
from parameterized import parameterized_class

from labels.models import Label
from labels.views import IndexView as LabelIndexView
from labels.views import LabelCreationView, LabelDeleteView, LabelUpdateView
from statuses.models import Status
from statuses.views import IndexView as StatusIndexView
from statuses.views import StatusCreationView, StatusDeleteView, StatusUpdateView
from task_manager.misc import get_test_data
from task_manager.views import IndexView
from tasks.models import Task
from tasks.views import IndexView as TaskIndexView
from tasks.views import TaskCreationView, TaskDeleteView, TaskUpdateView
from users.models import User
from users.views import IndexView as UserIndexView
from users.views import UserCreationView, UserDeleteView, UserLoginView, UserUpdateView

test_data = get_test_data()

user = test_data['users']['has_relationships']
status = test_data['statuses']['existing']
label = test_data['labels']['existing']
task = test_data['tasks']['existing']


class ViewsTest(TestCase):
    """Views tests."""

    def test_index_page(self):
        response = self.client.get(reverse_lazy('index'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            IndexView.as_view().__name__,
        )

    def test_login_page(self):
        response = self.client.get(reverse_lazy('login'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'layouts/form.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            UserLoginView.as_view().__name__,
        )


@parameterized_class(
    ('model', 'url', 'template', 'view'),
    [
        (
            User,
            'users:index',
            'users/user_list.html',
            UserIndexView,
        ),
        (
            Status,
            'statuses:index',
            'statuses/status_list.html',
            StatusIndexView,
        ),
        (
            Label,
            'labels:index',
            'labels/label_list.html',
            LabelIndexView,
        ),
        (
            Task,
            'tasks:index',
            'tasks/task_list.html',
            TaskIndexView,
        ),
    ],
)
class ListPageTest(TestCase):
    """List pages view tests."""

    fixtures = ['data.json']

    def test_list_page(self):
        self.client.login(
            username=user['username'],
            password=user['password'],
        )
        data_list = self.model.objects.all()
        response = self.client.get(reverse_lazy(self.url))

        self.assertQuerysetEqual(
            response.context['object_list'],
            data_list,
            ordered=False,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(
            response.resolver_match.func.__name__,
            self.view.as_view().__name__,
        )


@parameterized_class(
    ('url', 'id', 'template', 'view'),
    [
        (
            'users:create',
            None,
            'layouts/form.html',
            UserCreationView,
        ),
        (
            'users:update',
            [user['pk']],
            'layouts/form.html',
            UserUpdateView,
        ),
        (
            'users:delete',
            [user['pk']],
            'delete.html',
            UserDeleteView,
        ),
        (
            'statuses:create',
            None,
            'layouts/form.html',
            StatusCreationView,
        ),
        (
            'statuses:update',
            [status['pk']],
            'layouts/form.html',
            StatusUpdateView,
        ),
        (
            'statuses:delete',
            [status['pk']],
            'delete.html',
            StatusDeleteView,
        ),
        (
            'labels:create',
            None,
            'layouts/form.html',
            LabelCreationView,
        ),
        (
            'labels:update',
            [label['pk']],
            'layouts/form.html',
            LabelUpdateView,
        ),
        (
            'labels:delete',
            [label['pk']],
            'delete.html',
            LabelDeleteView,
        ),
        (
            'tasks:create',
            None,
            'layouts/form.html',
            TaskCreationView,
        ),
        (
            'tasks:update',
            [task['pk']],
            'layouts/form.html',
            TaskUpdateView,
        ),
        (
            'tasks:delete',
            [task['pk']],
            'delete.html',
            TaskDeleteView,
        ),
    ],
)
class CRUDPageTest(TestCase):
    """CRUD pages view tests."""

    fixtures = ['data.json']

    def test_crud_page(self):
        self.client.login(
            username=user['username'],
            password=user['password'],
        )

        response = self.client.get(reverse_lazy(self.url, args=self.id))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(
            response.resolver_match.func.__name__,
            self.view.as_view().__name__,
        )
