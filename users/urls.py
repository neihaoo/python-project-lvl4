"""Users application URL Configuration."""

from django.urls import path

from users.views import IndexView, UserCreationView, UserDeleteView, UserUpdateView

app_name = 'users'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', UserCreationView.as_view(), name='create'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
]
