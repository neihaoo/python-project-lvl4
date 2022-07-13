"""Tasks application models."""

from django.db import models
from statuses.models import Status
from users.models import User


class Task(models.Model):
    """Task model."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    executor = models.ForeignKey(
        User,
        models.PROTECT,
        null=True,
        blank=True,
        related_name='executor',
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Represent the model as a string."""
        return self.name
