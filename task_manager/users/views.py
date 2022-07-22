"""Users application Views."""

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import (
    NoPermissionMixin,
    ProtectedErrorMixin,
    UserLoginRequiredMixin,
)
from task_manager.users.forms import UserCreateForm

CREATION_SUCCESS_MESSAGE = _('User successfully registered.')
UPDATE_SUCCESS_MESSAGE = _('User successfully changed.')
DELETE_SUCCESS_MESSAGE = _('User successfully deleted.')

LOGIN_SUCCESS_MESSAGE = _('You are logged in.')
LOGOUT_SUCCESS_MESSAGE = _('You are unlogged.')

PERMISSION_DENIED_MESSAGE = _('You have no rights to change another user.')
PROTECTED_ERROR_MESSAGE = _('Unable to delete the user because it is in use.')


class IndexView(ListView):
    """Users page view."""

    model = get_user_model()


class UserCreationView(SuccessMessageMixin, CreateView):
    """User creation page view."""

    model = get_user_model()
    form_class = UserCreateForm
    template_name = 'layouts/form.html'
    success_url = reverse_lazy('login')
    success_message = CREATION_SUCCESS_MESSAGE
    extra_context = {
        'header': _('Registration'),
        'button': _('Register'),
    }

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('index'))

        return super().get(request, *args, **kwargs)


class UserUpdateView(
    UserLoginRequiredMixin,
    NoPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
):
    """Update user page view."""

    model = get_user_model()
    form_class = UserCreateForm
    template_name = 'layouts/form.html'
    success_url = reverse_lazy('users:index')
    success_message = UPDATE_SUCCESS_MESSAGE
    permission_denied_url = reverse_lazy('users:index')
    permission_denied_message = PERMISSION_DENIED_MESSAGE
    extra_context = {
        'header': _('Changing the user'),
        'button': _('Change'),
    }

    def test_func(self):
        user = self.get_object()

        return self.request.user == user


class UserDeleteView(
    UserLoginRequiredMixin,
    NoPermissionMixin,
    ProtectedErrorMixin,
    SuccessMessageMixin,
    DeleteView,
):
    """Delete user page view."""

    model = get_user_model()
    template_name = 'delete.html'
    success_url = reverse_lazy('users:index')
    protected_error_url = reverse_lazy('users:index')
    success_message = DELETE_SUCCESS_MESSAGE
    permission_denied_url = reverse_lazy('users:index')
    permission_denied_message = PERMISSION_DENIED_MESSAGE
    protected_error_message = PROTECTED_ERROR_MESSAGE
    extra_context = {
        'header': _('Deleting a user'),
        'button': _('Yes, delete'),
    }

    def test_func(self):
        user = self.get_object()

        return self.request.user == user


class UserLoginView(SuccessMessageMixin, LoginView):
    """Login page view."""

    template_name = 'layouts/form.html'
    next_page = reverse_lazy('index')
    redirect_authenticated_user = True
    success_url = reverse_lazy('users:index')
    success_message = LOGIN_SUCCESS_MESSAGE
    extra_context = {
        'header': _('Login'),
        'button': _('Log in'),
    }


class UserLogoutView(LogoutView):
    """Logout page view."""

    next_page = reverse_lazy('index')
    success_message = LOGOUT_SUCCESS_MESSAGE

    def dispatch(self, request, *args, **kwargs):
        """Take in the request and returns the response."""
        messages.info(request, self.success_message)

        return super().dispatch(request, *args, **kwargs)
