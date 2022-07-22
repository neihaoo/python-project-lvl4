"""Project filter tests."""

from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.misc import get_test_data
from task_manager.tasks.models import Task


class TaskFilterTest(TestCase):
    """Task filters test."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data()

    def setUp(self):
        user = self.test_data['users']['has_relationships']

        self.client.login(
            username=user['username'],
            password=user['password'],
        )

    def test_status_filter(self):
        status = self.test_data['statuses']['has_relationships']
        response = self.client.get(
            reverse_lazy('tasks:index'),
            {'status': status['pk']},
        )
        filtered_tasks = Task.objects.filter(status_id=status['pk'])

        self.assertQuerysetEqual(
            response.context['task_list'],
            filtered_tasks,
            ordered=False,
        )

    def test_executor_filter(self):
        executor = self.test_data['users']['has_relationships']
        response = self.client.get(
            reverse_lazy('tasks:index'),
            {'executor': executor['pk']},
        )
        filtered_tasks = Task.objects.filter(executor_id=executor['pk'])

        self.assertQuerysetEqual(
            response.context['task_list'],
            filtered_tasks,
            ordered=False,
        )

    def test_label_filter(self):
        label = self.test_data['labels']['has_relationships']
        response = self.client.get(reverse_lazy('tasks:index'), {'label': label['pk']})
        filtered_tasks = Task.objects.filter(labels__id=label['pk'])

        self.assertQuerysetEqual(
            response.context['task_list'],
            filtered_tasks,
            ordered=False,
        )

    def test_author_filter(self):
        response = self.client.get(reverse_lazy('tasks:index'), {'self_tasks': 'on'})
        user = response.wsgi_request.user
        filtered_tasks = Task.objects.filter(created_by=user)

        self.assertQuerysetEqual(
            response.context['task_list'],
            filtered_tasks,
            ordered=False,
        )
