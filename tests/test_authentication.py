"""Project authentication tests."""

from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.misc import get_response_messages, get_test_data
from users.views import LOGIN_SUCCESS_MESSAGE, LOGOUT_SUCCESS_MESSAGE


class UserAuthenticationTest(TestCase):
    """User authentication tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        cls.user = test_data['users']['existing']

    def test_login(self):
        response = self.client.post(reverse_lazy('login'), self.user)
        response_messages = get_response_messages(response)

        self.assertIn(LOGIN_SUCCESS_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('index'))

    def test_logout(self):
        self.client.login(
            username=self.user['username'],
            password=self.user['password'],
        )

        response = self.client.post(reverse_lazy('logout'))
        response_messages = get_response_messages(response)

        self.assertIn(LOGOUT_SUCCESS_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('index'))
