

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('full_name', models.CharField(max_length=150, verbose_name='Ф. И. О.')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Получатель рассылки (Клиент)',
                'verbose_name_plural': 'Получатели рассылки (Клиенты)',
                'ordering': ['email'],
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_send_time', models.DateTimeField(verbose_name='Дата и время первой отправки')),
                ('end_time', models.DateTimeField(verbose_name='Дата и время окончания отправки')),
                ('status', models.CharField(choices=[('created', 'Создана'), ('started', 'Запущена'), ('completed', 'Завершена')], default='created', max_length=10, verbose_name='Статус рассылки')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
                ('recipients', models.ManyToManyField(to='mailing.client', verbose_name='Получатели')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
                'ordering': ['-first_send_time'],
            },
        ),
        migrations.CreateModel(
            name='MailingAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')),
                ('status', models.CharField(choices=[('success', 'Успешно'), ('failed', 'Не успешно')], max_length=10, verbose_name='Статус попытки')),
                ('server_response', models.TextField(blank=True, null=True, verbose_name='Ответ почтового сервера')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Попытка рассылки',
                'verbose_name_plural': 'Попытки рассылок',
                'ordering': ['-attempt_time'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='Тема письма')),
                ('body', models.TextField(verbose_name='Тело письма')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Сообщение для рассылки',
                'verbose_name_plural': 'Сообщения для рассылки',
                'ordering': ['subject'],
            },
        ),
        migrations.AddField(
            model_name='mailing',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mailing.message', verbose_name='Сообщение'),
        ),
    ]
