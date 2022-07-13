"""User application configuration."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Users config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
