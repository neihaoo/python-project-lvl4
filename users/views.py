"""Users View Module."""
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from users.forms import SiteUserChangeForm, SiteUserCreationForm
from users.mixins import UserPermissionMixin

users_messages = {
    'creation_success': _('User successfully registered'),
    'update_success': _('User has been successfully changed'),
    'delete_success': _('User successfully deleted'),
    'login_success': _('You are logged in'),
    'logout_success': _('You are unlogged'),
}


class IndexView(ListView):
    """Users page view."""

    model = get_user_model()
    template_name = 'users/index.html'


class UserCreationView(SuccessMessageMixin, CreateView):
    """User creation page view."""

    model = get_user_model()
    form_class = SiteUserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = users_messages['creation_success']


class UserUpdateView(UserPermissionMixin, SuccessMessageMixin, UpdateView):
    """Update user page view."""

    model = get_user_model()
    form_class = SiteUserChangeForm
    template_name = 'users/update.html'
    success_message = users_messages['update_success']


class UserDeleteView(UserPermissionMixin, SuccessMessageMixin, DeleteView):
    """Delete user page view."""

    model = get_user_model()
    template_name = 'users/delete.html'
    success_message = users_messages['delete_success']


class UserLoginView(SuccessMessageMixin, LoginView):
    """Login user page view."""

    template_name = 'users/login.html'
    next_page = reverse_lazy('index')
    success_message = users_messages['login_success']


class UserLogoutView(LogoutView):
    """Logout user page view."""

    next_page = reverse_lazy('index')
    success_message = users_messages['logout_success']

    def dispatch(self, request, *args, **kwargs):
        """Take in the request and returns the response."""
        messages.info(request, _(self.success_message))

        return super().dispatch(request, *args, **kwargs)
