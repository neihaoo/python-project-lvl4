"""Labels application models."""

from django.db import models
from django.utils.translation import gettext_lazy as _

MAX_LENGTH = 100


class Label(models.Model):
    """Label model."""

    name = models.CharField(max_length=MAX_LENGTH, unique=True, verbose_name=_('Name'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Represent the model as a string."""
        return self.name
