# users/views.py

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView # Добавляем UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin # <--- ВОТ ЭТА СТРОКА БЫЛА ПРОПУЩЕНА!
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .forms import RegisterForm, UserProfileForm # Импортируем новую форму
from .models import User

class RegisterView(CreateView):
    """
    Представление для регистрации нового пользователя.
    """
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        send_mail(
            subject='Добро пожаловать в наш интернет-магазин!',
            message=f'Привет, {user.email}! Спасибо за регистрацию в нашем интернет-магазине. Мы рады видеть тебя!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return response

class CustomLoginView(LoginView):
    """
    Кастомное представление для авторизации пользователя.
    """
    template_name = 'users/login.html'
    fields = ['email', 'password']
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('catalog:product_list')



class ProfileUpdateView(LoginRequiredMixin, UpdateView): # Теперь LoginRequiredMixin будет определен
    """
    Представление для редактирования профиля авторизованного пользователя.
    """
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile_edit')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при обновлении профиля. Проверьте данные.")
        return super().form_invalid(form)