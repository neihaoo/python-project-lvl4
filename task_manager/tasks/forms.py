"""Tasks application forms."""

from django.forms import ModelForm

from task_manager.tasks.models import Task


class TaskForm(ModelForm):
    """Task form."""

    class Meta(object):
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'labels')
