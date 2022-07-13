"""User application forms."""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    """User form."""

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username')
