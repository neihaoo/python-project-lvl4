"""Statuses application URL Configuration."""

from django.urls import path

from task_manager.statuses.views import (
    IndexView,
    StatusCreationView,
    StatusDeleteView,
    StatusUpdateView,
)

app_name = 'statuses'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', StatusCreationView.as_view(), name='create'),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name='delete'),
]
