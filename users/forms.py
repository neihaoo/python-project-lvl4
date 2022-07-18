"""User application forms."""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

MAX_LENGTH = 150


class UserCreateForm(UserCreationForm):
    """User form."""

    first_name = forms.CharField(max_length=MAX_LENGTH, required=True)
    last_name = forms.CharField(max_length=MAX_LENGTH, required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username')
