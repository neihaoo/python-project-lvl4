"""Labels application views."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.mixins import ProtectedErrorMixin, UserLoginRequiredMixin

CREATION_SUCCESS_MESSAGE = _('Label successfully created.')
UPDATE_SUCCESS_MESSAGE = _('Label successfully changed.')
DELETE_SUCCESS_MESSAGE = _('Label successfully deleted.')

PROTECTED_ERROR_MESSAGE = _('Unable to delete the label because it is in use.')


class IndexView(UserLoginRequiredMixin, ListView):
    """Labels page view."""

    model = Label


class LabelCreationView(
    UserLoginRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    """Label creation page view."""

    model = Label
    form_class = LabelForm
    template_name = 'layouts/form.html'
    success_url = reverse_lazy('labels:index')
    success_message = CREATION_SUCCESS_MESSAGE
    extra_context = {
        'header': _('Create a label'),
        'button': _('Create'),
    }


class LabelUpdateView(
    UserLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    """Update label page view."""

    model = Label
    form_class = LabelForm
    template_name = 'layouts/form.html'
    success_url = reverse_lazy('labels:index')
    success_message = UPDATE_SUCCESS_MESSAGE
    extra_context = {
        'header': _('Changing label'),
        'button': _('Change'),
    }


class LabelDeleteView(
    UserLoginRequiredMixin,
    ProtectedErrorMixin,
    SuccessMessageMixin,
    DeleteView,
):
    """Delete label page view."""

    model = Label
    template_name = 'delete.html'
    success_url = reverse_lazy('labels:index')
    protected_error_url = reverse_lazy('labels:index')
    success_message = DELETE_SUCCESS_MESSAGE
    protected_error_message = PROTECTED_ERROR_MESSAGE
    extra_context = {
        'header': _('Label deletion'),
        'button': _('Yes, delete'),
    }
