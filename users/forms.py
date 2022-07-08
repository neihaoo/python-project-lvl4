"""Users forms."""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SiteUserCreationForm(UserCreationForm):
    """Site user creation form."""

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username')


class SiteUserChangeForm(SiteUserCreationForm):
    """Site user change form."""
