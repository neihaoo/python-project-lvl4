"""Application Views."""

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from users.forms import UserForm
from users.mixins import UserPermissionMixin

user_messages = {
    'creation_success': _('User successfully registered'),
    'update_success': _('User has been successfully changed'),
    'delete_success': _('User successfully deleted'),
    'login_success': _('You are logged in'),
    'logout_success': _('You are unlogged'),
}


class IndexView(ListView):
    """Users page view."""

    model = get_user_model()


class UserCreationView(SuccessMessageMixin, CreateView):
    """User creation page view."""

    model = get_user_model()
    form_class = UserForm
    template_name = 'layouts/form.html'
    success_url = reverse_lazy('login')
    success_message = user_messages['creation_success']
    extra_context = {
        'header': _('Registration'),
        'button': _('Register'),
    }


class UserUpdateView(UserPermissionMixin, SuccessMessageMixin, UpdateView):
    """Update user page view."""

    model = get_user_model()
    form_class = UserForm
    template_name = 'layouts/form.html'
    success_url = reverse_lazy('users:index')
    success_message = user_messages['update_success']
    extra_context = {
        'header': _('Changing the user'),
        'button': _('Change'),
    }


class UserDeleteView(UserPermissionMixin, SuccessMessageMixin, DeleteView):
    """Delete user page view."""

    model = get_user_model()
    template_name = 'delete.html'
    success_message = user_messages['delete_success']
    success_url = reverse_lazy('users:index')
    extra_context = {
        'header': _('Deleting a user'),
        'button': _('Yes, delete'),
    }


class UserLoginView(SuccessMessageMixin, LoginView):
    """Login page view."""

    template_name = 'layouts/form.html'
    next_page = reverse_lazy('index')
    success_url = reverse_lazy('users:index')
    success_message = user_messages['login_success']
    extra_context = {
        'header': _('Login'),
        'button': _('Log in'),
    }


class UserLogoutView(LogoutView):
    """Logout page view."""

    next_page = reverse_lazy('index')
    success_message = user_messages['logout_success']

    def dispatch(self, request, *args, **kwargs):
        """Take in the request and returns the response."""
        messages.info(request, self.success_message)

        return super().dispatch(request, *args, **kwargs)
