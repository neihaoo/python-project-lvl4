"""Labels application configuration."""

from django.apps import AppConfig


class LabelsConfig(AppConfig):
    """Labels config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_manager.labels'
