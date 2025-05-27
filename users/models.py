# users/models.py

from django.contrib.auth.models import AbstractUser, UserManager # <--- Добавляем UserManager
from django.db import models

class CustomUserManager(UserManager): # <--- НОВЫЙ КЛАСС МЕНЕДЖЕРА
    """
    Кастомный менеджер пользователей, который использует email как username
    для создания пользователя и суперпользователя.
    """
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Кастомная модель пользователя, отнаследованная от AbstractUser.
    Использует email в качестве поля для авторизации.
    """
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name='Страна')

    username = None # Удаляем поле username

    USERNAME_FIELD = 'email'  # Устанавливаем email в качестве поля для авторизации
    REQUIRED_FIELDS = [] # Больше не требуется username

    objects = CustomUserManager() # <--- УКАЗЫВАЕМ НАШ КУСТОМНЫЙ МЕНЕДЖЕР

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']

    def __str__(self):
        return self.email