"""Labels application URL Configuration."""

from django.urls import path

from labels.views import IndexView, LabelCreationView, LabelDeleteView, LabelUpdateView

app_name = 'labels'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', LabelCreationView.as_view(), name='create'),
    path('<int:pk>/update/', LabelUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', LabelDeleteView.as_view(), name='delete'),
]
