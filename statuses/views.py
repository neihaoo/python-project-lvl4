"""Statuses application views."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from statuses.forms import StatusForm
from statuses.models import Status
from task_manager.mixins import ProtectedErrorMixin, UserLoginRequiredMixin
from users.views import LOGIN_REQUIRED_MESSAGE

CREATION_SUCCESS_MESSAGE = _('Status successfully created')
UPDATE_SUCCESS_MESSAGE = _('Status successfully changed')
DELETE_SUCCESS_MESSAGE = _('Status successfully deleted')

PROTECTED_ERROR_MESSAGE = _('Unable to delete status because it is in use')


class IndexView(UserLoginRequiredMixin, ListView):
    """Statuses page view."""

    model = Status
    login_url = reverse_lazy('login')
    login_required_message = LOGIN_REQUIRED_MESSAGE


class StatusCreationView(
    UserLoginRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    """Status creation page view."""

    model = Status
    form_class = StatusForm
    template_name = 'layouts/form.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('statuses:index')
    login_required_message = LOGIN_REQUIRED_MESSAGE
    success_message = CREATION_SUCCESS_MESSAGE
    extra_context = {
        'header': _('Create a status'),
        'button': _('Create'),
    }


class StatusUpdateView(
    UserLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    """Update status page view."""

    model = Status
    form_class = StatusForm
    template_name = 'layouts/form.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('statuses:index')
    login_required_message = LOGIN_REQUIRED_MESSAGE
    success_message = UPDATE_SUCCESS_MESSAGE
    extra_context = {
        'header': _('Changing status'),
        'button': _('Change'),
    }


class StatusDeleteView(
    UserLoginRequiredMixin,
    ProtectedErrorMixin,
    SuccessMessageMixin,
    DeleteView,
):
    """Delete status page view."""

    model = Status
    template_name = 'delete.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('statuses:index')
    protected_error_url = reverse_lazy('statuses:index')
    login_required_message = LOGIN_REQUIRED_MESSAGE
    success_message = DELETE_SUCCESS_MESSAGE
    protected_error_message = PROTECTED_ERROR_MESSAGE
    extra_context = {
        'header': _('Status deletion'),
        'button': _('Yes, delete'),
    }
