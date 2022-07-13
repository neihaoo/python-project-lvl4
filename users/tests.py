"""Users application tests."""

from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse_lazy
from parameterized import parameterized_class
from task_manager.misc import get_response_messages, get_test_data
from users import views
from users.models import User


class UserViewsTest(TestCase):
    """User views tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        user = test_data['users']['existing_user']

        cls.user = User.objects.get(username=user['username'])

    def setUp(self):
        self.client.force_login(self.user)

    def test_index_page(self):
        users = User.objects.all()
        response = self.client.get(reverse_lazy('users:index'))

        self.assertQuerysetEqual(
            response.context['user_list'],
            users,
            ordered=False,
        )
        self.assertTemplateUsed(response, 'users/user_list.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.IndexView.as_view().__name__,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_page(self):
        self.client.logout()

        response = self.client.get(reverse_lazy('users:create'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'layouts/form.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.UserCreationView.as_view().__name__,
        )

    def test_update_page(self):
        response = self.client.get(
            reverse_lazy('users:update', args=[self.user.pk]),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'layouts/form.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.UserUpdateView.as_view().__name__,
        )

    def test_delete_page(self):
        response = self.client.get(
            reverse_lazy('users:delete', args=[self.user.pk]),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'delete.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.UserDeleteView.as_view().__name__,
        )

    def test_login_page(self):
        self.client.logout()

        response = self.client.get(reverse_lazy('login'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'layouts/form.html')
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.UserLoginView.as_view().__name__,
        )


class UserCRUDTest(TestCase):
    """User CRUD tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        user = test_data['users']['another_user']

        cls.new_user = test_data['users']['new_user']
        cls.user = User.objects.get(username=user['username'])

    def setUp(self):
        self.client.force_login(self.user)

    def test_create(self):
        self.client.logout()

        response = self.client.post(
            reverse_lazy('users:create'),
            {
                'username': self.new_user['username'],
                'password1': self.new_user['password'],
                'password2': self.new_user['password'],
            },
        )
        response_messages = get_response_messages(response)
        created_user = User.objects.get(username=self.new_user['username'])

        self.assertIn(views.CREATION_SUCCESS_MESSAGE, response_messages)
        self.assertEqual(self.new_user['username'], created_user.username)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_update(self):
        response = self.client.post(
            reverse_lazy('users:update', args=[self.user.pk]),
            {
                'username': self.new_user['username'],
                'password1': self.new_user['password'],
                'password2': self.new_user['password'],
            },
        )
        response_messages = get_response_messages(response)
        updated_user = User.objects.get(pk=self.user.pk)

        self.assertIn(views.UPDATE_SUCCESS_MESSAGE, response_messages)
        self.assertEqual(self.new_user['username'], updated_user.username)
        self.assertRedirects(response, reverse_lazy('users:index'))

    def test_delete(self):
        response = self.client.post(
            reverse_lazy('users:delete', args=[self.user.pk]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(views.DELETE_SUCCESS_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('users:index'))

        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=self.user.pk)


class UserAuthorisationTest(TestCase):
    """User authorisation tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        cls.user = test_data['users']['existing_user']

    def test_login(self):
        response = self.client.post(reverse_lazy('login'), self.user)
        response_messages = get_response_messages(response)

        self.assertIn(views.LOGIN_SUCCESS_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('index'))

    def test_logout(self):
        self.client.login(
            username=self.user['username'],
            password=self.user['password'],
        )

        response = self.client.post(reverse_lazy('logout'))
        response_messages = get_response_messages(response)

        self.assertIn(views.LOGOUT_SUCCESS_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('index'))


@parameterized_class('url', [('users:update',), ('users:delete',)])
class UserPermissionTest(TestCase):
    """User permissions tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        user = test_data['users']['existing_user']
        another_user = test_data['users']['another_user']

        cls.user = User.objects.get(username=user['username'])
        cls.another_user = User.objects.get(username=another_user['username'])

    def test_permission_denied(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse_lazy(self.url, args=[self.another_user.pk]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(views.PERMISSION_DENIED_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('users:index'))

    def test_login_required(self):
        response = self.client.get(
            reverse_lazy(self.url, args=[self.user.pk]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(views.LOGIN_REQUIRED_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('login'))


class UserErrorTest(TestCase):
    """User errors tests."""

    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        test_data = get_test_data()

        user = test_data['users']['existing_user']

        cls.user = User.objects.get(username=user['username'])

    def test_protected_error(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse_lazy('users:delete', args=[self.user.pk]),
        )
        response_messages = get_response_messages(response)

        self.assertIn(views.PROTECTED_ERROR_MESSAGE, response_messages)
        self.assertRedirects(response, reverse_lazy('users:index'))
