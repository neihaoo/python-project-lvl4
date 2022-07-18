"""Users application models."""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Model representing a user account."""

    def __str__(self):
        """Represent the model as a string."""
        return self.get_full_name()
