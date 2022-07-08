"""Task Manager URL Configuration."""

from django.contrib import admin
from django.urls import include, path
from task_manager.view import IndexView
from users.views import UserLoginView, UserLogoutView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('users/', include('users.urls')),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]
