"""Labels application admin interface."""

from django.contrib import admin

from task_manager.labels.models import Label


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    """Admin interface configuretion."""

    list_display = ('name', 'created_at')
