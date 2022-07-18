"""Tasks application models."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from labels.models import Label
from statuses.models import Status
from users.models import User


class Task(models.Model):
    """Task model."""

    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Status'),
    )
    executor = models.ForeignKey(
        User,
        models.PROTECT,
        null=True,
        blank=True,
        related_name='executor',
        verbose_name=_('Executor'),
    )
    labels = models.ManyToManyField(
        Label,
        through='Relationships',
        blank=True,
        verbose_name=_('Labels'),
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_by',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Represent the model as a string."""
        return self.name


class Relationships(models.Model):
    """Intermediary model."""

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
