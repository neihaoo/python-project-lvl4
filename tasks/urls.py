"""Tasks application URL Configuration."""

from django.urls import path

from tasks.views import IndexView, TaskCreationView, TaskDeleteView, TaskUpdateView

app_name = 'tasks'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', TaskCreationView.as_view(), name='create'),
    path('create/<int:pk>/update/', TaskUpdateView.as_view(), name='update'),
    path('create/<int:pk>/delete/', TaskDeleteView.as_view(), name='delete'),
]
