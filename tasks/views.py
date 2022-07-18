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
from tasks.filters import TasktFilter
from tasks.forms import TaskForm
from tasks.models import Task
from users.views import LOGIN_REQUIRED_MESSAGE

CREATION_SUCCESS_MESSAGE = _('Task successfully created.')
UPDATE_SUCCESS_MESSAGE = _('Task successfully changed.')
DELETE_SUCCESS_MESSAGE = _('Task successfully deleted.')

PERMISSION_DENIED_MESSAGE = _('Only the author of the task can delete it.')


class IndexView(UserLoginRequiredMixin, FilterView, ListView):
    """Tasks page view."""

    model = Task
    filterset_class = TasktFilter
    template_name = 'tasks/task_list.html'
    login_url = reverse_lazy('login')
    login_required_message = LOGIN_REQUIRED_MESSAGE


class TaskDetailView(UserLoginRequiredMixin, DetailView):
    """Tasks detail view."""

    model = Task
    login_url = reverse_lazy('login')
    login_required_message = LOGIN_REQUIRED_MESSAGE


class TaskCreationView(UserLoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Task creation page view."""

    model = Task
    form_class = TaskForm
    template_name = 'layouts/form.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('tasks:index')
    login_required_message = LOGIN_REQUIRED_MESSAGE
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
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('tasks:index')
    login_required_message = LOGIN_REQUIRED_MESSAGE
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
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('tasks:index')
    permission_denied_url = reverse_lazy('tasks:index')
    login_required_message = LOGIN_REQUIRED_MESSAGE
    success_message = DELETE_SUCCESS_MESSAGE
    permission_denied_message = PERMISSION_DENIED_MESSAGE
    extra_context = {
        'header': _('Task deletion'),
        'button': _('Yes, delete'),
    }

    def test_func(self):
        task = self.get_object()

        return self.request.user == task.created_by
