"""Application admin interface."""

from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface configuretion."""

    list_display = ('username', 'first_name', 'last_name', 'date_joined')
