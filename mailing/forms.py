# mailing/forms.py

from django import forms
from .models import Client, Message, Mailing
from django.utils import timezone
from django.core.exceptions import ValidationError


class MessageForm(forms.ModelForm):
    """
    Форма для создания и редактирования сообщений.
    """

    class Meta:
        model = Message
        fields = ('subject', 'body')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'subject':
                field.widget.attrs['placeholder'] = 'Введите тему письма'
            elif field_name == 'body':
                field.widget.attrs['placeholder'] = 'Введите текст письма'


class ClientForm(forms.ModelForm):
    """
    Форма для создания и редактирования получателей рассылки (клиентов).
    """

    class Meta:
        model = Client
        fields = ('email', 'full_name', 'comment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'email':
                field.widget.attrs['placeholder'] = 'Введите email клиента'
            elif field_name == 'full_name':
                field.widget.attrs['placeholder'] = 'Введите Ф. И. О. клиента'
            elif field_name == 'comment':
                field.widget.attrs['placeholder'] = 'Комментарий (необязательно)'


class MailingForm(forms.ModelForm):
    """
    Форма для создания и редактирования рассылок.
    """

    class Meta:
        model = Mailing
        fields = ('first_send_time', 'end_time', 'message', 'recipients')
        widgets = {
            'first_send_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'recipients': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'message': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['message'].queryset = Message.objects.filter(owner=user)
            self.fields['recipients'].queryset = Client.objects.filter(owner=user)

        for field_name, field in self.fields.items():
            if field_name not in ['first_send_time', 'end_time', 'recipients', 'message']:
                field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        first_send_time = cleaned_data.get('first_send_time')
        end_time = cleaned_data.get('end_time')

        errors = {}

        if first_send_time and first_send_time < timezone.now():
            errors['first_send_time'] = "Дата и время первой отправки не могут быть в прошлом."

        if first_send_time and end_time and end_time <= first_send_time:
            errors['end_time'] = "Дата и время окончания отправки должны быть позже даты первой отправки."

        if errors:
            raise ValidationError(errors)

        return cleaned_data