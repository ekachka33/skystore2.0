# users/urls.py

from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from .views import RegisterView, CustomLoginView, ProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    # Используй CustomLogoutView.as_view(), если ты его реализовал по варианту 2,
    # иначе LogoutView.as_view(next_page=reverse_lazy('users:login'))
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('users:login')), name='logout'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]