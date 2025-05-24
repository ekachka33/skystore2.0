# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    """
    Форма для регистрации нового пользователя.
    Использует email в качестве поля для авторизации.
    """
    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Введите ваш email'})
        # Удаляем поле username, так как мы используем email для авторизации
        # Убедимся, что оно существует перед удалением, чтобы избежать ошибок,
        # если базовый класс UserCreationForm изменится.
        if 'username' in self.fields:
            del self.fields['username']

    def clean_email(self):
        email = self.cleaned_data['email']
        # При регистрации проверяем, что email не занят
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email # Присваиваем email в качестве username, чтобы AbstractUser мог работать
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """
    Форма для редактирования профиля пользователя.
    """
    class Meta:
        model = User
        fields = ('email', 'avatar', 'phone_number', 'country') # Поля, которые можно редактировать

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем placeholder'ы и, возможно, стили для полей
        for field_name in self.fields:
            # Аватар - это поле для загрузки файла, не нужно добавлять placeholder и class form-control к нему
            if field_name not in ['avatar', 'password', 'password2']: # Убедимся, что и к паролям не применяем
                self.fields[field_name].widget.attrs['placeholder'] = self.fields[field_name].label
                self.fields[field_name].widget.attrs['class'] = 'form-control' # Добавляем класс Bootstrap
            elif field_name == 'avatar':
                self.fields[field_name].widget.attrs['class'] = 'form-control-file' # Специальный класс для файлов

        # Поле email должно быть заблокировано для редактирования, если это не требуется,
        # или обрабатываться по-особому. Но для данного задания оставим его редактируемым.

    def clean_email(self):
        email = self.cleaned_data['email']
        # При редактировании профиля нужно убедиться, что новый email не занят
        # другим пользователем (но может быть текущим пользователем)
        # self.instance.pk - это ID текущего редактируемого пользователя
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email