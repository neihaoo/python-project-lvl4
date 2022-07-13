"""Labels application models."""

from django.db import models


class Label(models.Model):
    """Label model."""

    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Represent the model as a string."""
        return self.name
