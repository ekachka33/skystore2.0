#mailing/models.py

from django.db import models
from django.conf import settings # Для ссылки на AUTH_USER_MODEL
from django.utils import timezone # Для работы с датами и временем


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=150, verbose_name='Ф. И. О.')
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    class Meta:
        verbose_name = 'Получатель рассылки (Клиент)'
        verbose_name_plural = 'Получатели рассылки (Клиенты)'
        ordering = ['email']


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылки'
        ordering = ['subject']


# Модель «Рассылка» (Mailing)
class Mailing(models.Model):
    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_COMPLETED = 'completed'
    STATUS_PAUSED = 'paused'

    STATUS_CHOICES = [
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_COMPLETED, 'Завершена'),
        (STATUS_PAUSED, 'Приостановлена'),
    ]

    first_send_time = models.DateTimeField(verbose_name='Дата и время первой отправки')
    end_time = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
        verbose_name='Статус рассылки'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        verbose_name='Сообщение',
        blank=True,
        null=True
    )
    recipients = models.ManyToManyField(Client, verbose_name='Получатели')

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Рассылка от {self.first_send_time.strftime('%Y-%m-%d %H:%M')} до {self.end_time.strftime('%Y-%m-%d %H:%M')} ({self.get_status_display()})"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['-first_send_time']

        permissions = [
            ("can_view_all_mailings", "Can view all mailings (for managers)"),
            ("can_deactivate_mailings", "Can deactivate/pause mailings (for managers)"),
        ]


class MailingAttempt(models.Model):
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = [
        (STATUS_SUCCESS, 'Успешно'),
        (STATUS_FAILED, 'Не успешно'),
    ]

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name='Рассылка'
    )
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name='Статус попытки'
    )
    server_response = models.TextField(verbose_name='Ответ почтового сервера', blank=True, null=True)

    def __str__(self):
        return f"Попытка для '{self.mailing.message.subject}' в {self.attempt_time.strftime('%Y-%m-%d %H:%M')} - {self.get_status_display()}"

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'
        ordering = ['-attempt_time']