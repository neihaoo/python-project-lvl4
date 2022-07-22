"""Statuses application configuration."""

from django.apps import AppConfig


class StatusesConfig(AppConfig):
    """Statuses config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_manager.statuses'
