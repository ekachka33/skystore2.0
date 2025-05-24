

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Кастомная модель пользователя, отнаследованная от AbstractUser.
    Использует email в качестве поля для авторизации.
    """
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name='Страна')

    USERNAME_FIELD = 'email'  # Устанавливаем email в качестве поля для авторизации
    REQUIRED_FIELDS = ['username'] # Здесь можно оставить 'username' или изменить, если он не нужен

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email'] # Можно отсортировать по email для удобства

    def __str__(self):
        return self.email
