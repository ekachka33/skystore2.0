# users/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, View  # Добавляем ListView и View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # Убедись, что эти импорты есть
from django.contrib import messages
from django.utils import timezone

from .models import User  # Импортируем нашу модель пользователя
from .forms import RegisterForm, UserProfileForm  # Импортируем формы


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.is_active = False
        response = super().form_valid(form)
        user = self.object
        messages.success(self.request, "Аккаунт создан. Пожалуйста, подтвердите ваш email (письмо отправлено).")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при регистрации. Проверьте данные.")
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    fields = ['email', 'password']
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('catalog:product_list')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
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


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Отображает список всех пользователей.
    Доступно только пользователям со статусом is_staff=True.
    """
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return User.objects.all().exclude(pk=self.request.user.pk)


class UserBlockView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Представление для блокировки/разблокировки пользователя.
    Доступно только пользователям со статусом is_staff=True.
    """

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, pk, *args, **kwargs):
        user_to_block = get_object_or_404(User, pk=pk)

        if user_to_block == self.request.user:
            messages.error(request, "Вы не можете заблокировать или разблокировать самого себя.")
            return redirect('users:user_list')

        if user_to_block.is_superuser and not self.request.user.is_superuser:
            messages.error(request, "Вы не можете заблокировать суперпользователя.")
            return redirect('users:user_list')

        user_to_block.is_active = not user_to_block.is_active
        user_to_block.save()

        if user_to_block.is_active:
            messages.success(request, f"Пользователь '{user_to_block.email}' разблокирован.")
        else:
            messages.warning(request, f"Пользователь '{user_to_block.email}' заблокирован.")

        return redirect('users:user_list')