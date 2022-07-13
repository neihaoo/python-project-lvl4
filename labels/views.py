"""Labels application views."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from labels.forms import LabelForm
from labels.models import Label
from task_manager.mixins import ProtectedErrorMixin, UserLoginRequiredMixin
from users.views import LOGIN_REQUIRED_MESSAGE

CREATION_SUCCESS_MESSAGE = _('Label successfully created')
UPDATE_SUCCESS_MESSAGE = _('Label successfully changed')
DELETE_SUCCESS_MESSAGE = _('Label successfully deleted')

PROTECTED_ERROR_MESSAGE = _('Unable to delete label because it is in use')


class IndexView(UserLoginRequiredMixin, ListView):
    """Labels page view."""

    model = Label
    login_url = reverse_lazy('login')
    login_required_message = LOGIN_REQUIRED_MESSAGE


class LabelCreationView(
    UserLoginRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    """Label creation page view."""

    model = Label
    form_class = LabelForm
    template_name = 'layouts/form.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('labels:index')
    login_required_message = LOGIN_REQUIRED_MESSAGE
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
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('labels:index')
    login_required_message = LOGIN_REQUIRED_MESSAGE
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
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('labels:index')
    protected_error_url = reverse_lazy('labels:index')
    login_required_message = LOGIN_REQUIRED_MESSAGE
    success_message = DELETE_SUCCESS_MESSAGE
    protected_error_message = PROTECTED_ERROR_MESSAGE
    extra_context = {
        'header': _('Label deletion'),
        'button': _('Yes, delete'),
    }
