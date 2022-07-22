"""Task manager project URL Configuration."""

from django.contrib import admin
from django.urls import include, path

from task_manager.users.views import UserLoginView, UserLogoutView
from task_manager.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('users/', include('task_manager.users.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]
