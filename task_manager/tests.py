"""Task Manager tests."""

from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from task_manager.view import IndexView


class TaskManagerTest(TestCase):
    """Test Task Manager views."""

    def test_index_page(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            IndexView.as_view().__name__,
        )
