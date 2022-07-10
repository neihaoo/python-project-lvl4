"""Application views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from statuses.forms import StatusForm
from statuses.models import Status

LOGIN_URL = 'login'

status_messages = {
    'creation_success': _('Status successfully created'),
    'update_success': _('Status successfully changed'),
    'delete_success': _('Status successfully deleted'),
}


class IndexView(LoginRequiredMixin, ListView):
    """Statuses page view."""

    model = Status
    login_url = reverse_lazy(LOGIN_URL)


class StatusCreationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Status creation page view."""

    model = Status
    form_class = StatusForm
    template_name = 'layouts/form.html'
    login_url = reverse_lazy(LOGIN_URL)
    success_url = reverse_lazy('statuses:index')
    success_message = status_messages['creation_success']
    extra_context = {
        'header': _('Create a status'),
        'button': _('Create'),
    }


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update status page view."""

    model = Status
    form_class = StatusForm
    template_name = 'layouts/form.html'
    login_url = reverse_lazy(LOGIN_URL)
    success_url = reverse_lazy('statuses:index')
    success_message = status_messages['update_success']
    extra_context = {
        'header': _('Changing status'),
        'button': _('Change'),
    }


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Delete user page view."""

    model = Status
    template_name = 'delete.html'
    login_url = reverse_lazy(LOGIN_URL)
    success_url = reverse_lazy('statuses:index')
    success_message = status_messages['delete_success']
    extra_context = {
        'header': _('Status deletion'),
        'button': _('Yes, delete'),
    }
