"""Tasks application views."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django_filters.views import FilterView

from task_manager.mixins import NoPermissionMixin, UserLoginRequiredMixin
from task_manager.tasks.filters import TasktFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task

CREATION_SUCCESS_MESSAGE = _('Task successfully created.')
UPDATE_SUCCESS_MESSAGE = _('Task successfully changed.')
DELETE_SUCCESS_MESSAGE = _('Task successfully deleted.')

PERMISSION_DENIED_MESSAGE = _('Only the author of the task can delete it.')


class IndexView(UserLoginRequiredMixin, FilterView, ListView):
    """Tasks page view."""

    model = Task
    filterset_class = TasktFilter
    template_name = 'tasks/task_list.html'


class TaskDetailView(UserLoginRequiredMixin, DetailView):
    """Tasks detail view."""

    model = Task


class TaskCreationView(UserLoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Task creation page view."""

    model = Task
    form_class = TaskForm
    template_name = 'layouts/form.html'
    success_url = reverse_lazy('tasks:index')
    success_message = CREATION_SUCCESS_MESSAGE
    extra_context = {
        'header': _('Create a task'),
        'button': _('Create'),
    }

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        return super().form_valid(form)


class TaskUpdateView(UserLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update Task page view."""

    model = Task
    form_class = TaskForm
    template_name = 'layouts/form.html'
    success_url = reverse_lazy('tasks:index')
    success_message = UPDATE_SUCCESS_MESSAGE
    extra_context = {
        'header': _('Changing task'),
        'button': _('Change'),
    }


class TaskDeleteView(
    UserLoginRequiredMixin,
    NoPermissionMixin,
    SuccessMessageMixin,
    DeleteView,
):
    """Delete task page view."""

    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('tasks:index')
    permission_denied_url = reverse_lazy('tasks:index')
    success_message = DELETE_SUCCESS_MESSAGE
    permission_denied_message = PERMISSION_DENIED_MESSAGE
    extra_context = {
        'header': _('Task deletion'),
        'button': _('Yes, delete'),
    }

    def test_func(self):
        task = self.get_object()

        return self.request.user == task.created_by
