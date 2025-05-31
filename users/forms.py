# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # Оставим UserChangeForm, так как он используется в админке по умолчанию
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

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """
    Форма для редактирования профиля пользователя.
    """
    class Meta:
        model = User
        fields = ('email', 'avatar', 'phone_number', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name not in ['avatar', 'password', 'password2']:
                self.fields[field_name].widget.attrs['placeholder'] = self.fields[field_name].label
                self.fields[field_name].widget.attrs['class'] = 'form-control'
            elif field_name == 'avatar':
                self.fields[field_name].widget.attrs['class'] = 'form-control-file'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email
