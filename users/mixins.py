"""Application mixins."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

permission_messages = {
    'login_required': _('You are not logged in! Please log in.'),
    'permission_denied': _('You have no rights to change another user.'),
}


class UserPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Users permission require mixin."""

    login_url = reverse_lazy('login')
    success_url = reverse_lazy('users:index')
    permission_denied_url = reverse_lazy('users:index')
    login_required_message = permission_messages['login_required']
    permission_denied_message = permission_messages['permission_denied']

    def test_func(self):
        user = self.get_object()

        return self.request.user == user

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, self.login_required_message)

            return redirect(self.login_url)

        messages.error(self.request, self.permission_denied_message)

        return redirect(self.permission_denied_url)
