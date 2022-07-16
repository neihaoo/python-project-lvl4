"""Statuses application admin interface."""

from django.contrib import admin

from statuses.models import Status


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Admin interface configuretion."""

    list_display = ('name', 'created_at')
