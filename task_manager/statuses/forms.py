"""Statuses application forms."""

from django.forms import ModelForm

from task_manager.statuses.models import Status


class StatusForm(ModelForm):
    """Status form."""

    class Meta(object):
        model = Status
        fields = ('name',)
