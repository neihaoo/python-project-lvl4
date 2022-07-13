"""Tasks application admin interface."""

from django.contrib import admin
from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin interface configuretion."""

    list_display = (
        'name',
        'description',
        'status',
        'executor',
        'created_by',
        'created_at',
    )
