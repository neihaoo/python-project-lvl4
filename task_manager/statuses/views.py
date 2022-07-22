"""Statuses application views."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import ProtectedErrorMixin, UserLoginRequiredMixin
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status

CREATION_SUCCESS_MESSAGE = _('Status successfully created.')
UPDATE_SUCCESS_MESSAGE = _('Status successfully changed.')
DELETE_SUCCESS_MESSAGE = _('Status successfully deleted.')

PROTECTED_ERROR_MESSAGE = _(
    'Unable to delete the status because it is in use.',
)


class IndexView(UserLoginRequiredMixin, ListView):
    """Statuses page view."""

    model = Status


class StatusCreationView(
    UserLoginRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    """Status creation page view."""

    model = Status
    form_class = StatusForm
    template_name = 'layouts/form.html'
    success_url = reverse_lazy('statuses:index')
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
    success_url = reverse_lazy('statuses:index')
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
    success_url = reverse_lazy('statuses:index')
    protected_error_url = reverse_lazy('statuses:index')
    success_message = DELETE_SUCCESS_MESSAGE
    protected_error_message = PROTECTED_ERROR_MESSAGE
    extra_context = {
        'header': _('Status deletion'),
        'button': _('Yes, delete'),
    }
