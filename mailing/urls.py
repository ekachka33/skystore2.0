# mailing/urls.py

from django.urls import path, reverse_lazy # Добавляем reverse_lazy, если его нет
from .views import (
    MessageListView,
    MessageDetailView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    ClientListView,
    ClientDetailView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    MailingListView,
    MailingDetailView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    MailingSendView,
    MailingAttemptListView,
    MailingToggleActiveView # Убедись, что все нужные View импортированы
)

app_name = 'mailing'

urlpatterns = [
    # URL-адреса для Сообщений
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    # URL-адреса для Получателей рассылки (Клиентов)
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    # URL-адреса для Рассылок
    path('', MailingListView.as_view(), name='mailing_list'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('<int:pk>/send/', MailingSendView.as_view(), name='mailing_send'),

    # URL-адреса для Попыток рассылок / Статистики
    path('attempts/', MailingAttemptListView.as_view(), name='attempt_list'),

    # URL-адрес для включения/отключения рассылки
    path('<int:pk>/toggle_active/', MailingToggleActiveView.as_view(), name='mailing_toggle_active'),
]