"""Tasks application filters."""

import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Label, Task


class TasktFilter(django_filters.FilterSet):
    """Tasks filte."""

    labels = django_filters.ModelChoiceFilter(
        label=_('Label'),
        queryset=Label.objects.all(),
    )
    self_tasks = django_filters.BooleanFilter(
        label=_('Only your own tasks'),
        method='filter_by_current_user',
        widget=forms.CheckboxInput,
    )

    def filter_by_current_user(self, queryset, query_name, query_value):
        author = getattr(self.request, 'user', None)

        return queryset.filter(created_by=author) if query_value else queryset

    class Meta(object):
        model = Task
        fields = ('status', 'executor', 'labels', 'self_tasks')
