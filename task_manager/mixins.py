"""Task manager project mixins."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

LOGIN_REQUIRED_MESSAGE = _('You are not logged in! Please log in.')


class ProtectedErrorMixin(object):
    """React on exception ProtectedError."""

    protected_error_message = ''
    protected_error_url = ''

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, self.protected_error_message)

            return redirect(self.protected_error_url)

        return response


class UserLoginRequiredMixin(LoginRequiredMixin):
    """Verify that the current user is authenticated."""

    login_url = reverse_lazy('login')
    login_required_message = LOGIN_REQUIRED_MESSAGE

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, self.login_required_message)

            return redirect(self.login_url)

        return super().dispatch(request, *args, **kwargs)


class NoPermissionMixin(UserPassesTestMixin):
    """Verify that the current user has a permisiion."""

    permission_denied_url = ''

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            messages.error(self.request, self.permission_denied_message)

            return redirect(self.permission_denied_url)

        return super().dispatch(request, *args, **kwargs)
