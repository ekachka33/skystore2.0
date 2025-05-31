# mailing/views.py

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from .models import Message, Client, Mailing, MailingAttempt
from .forms import MessageForm, ClientForm, MailingForm
from .services import send_single_mailing
from django.db.models import Count
from django.db.models import Q


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Сообщение успешно создано!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при создании сообщения. Проверьте введенные данные.")
        return super().form_invalid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Сообщение успешно обновлено!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при обновлении сообщения. Проверьте введенные данные.")
        return super().form_invalid(form)


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модератор продуктов').exists():
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    context_object_name = 'client'

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or \
            self.request.user.groups.filter(name='Модератор продуктов').exists()


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Получатель рассылки успешно создан!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при создании получателя. Проверьте введенные данные.")
        return super().form_invalid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Получатель рассылки успешно удален!")
        return super().form_valid(form)



class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модератор продуктов').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or \
            self.request.user.groups.filter(name='Модератор продуктов').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = self.object
        context['can_send_now'] = (mailing.status == Mailing.STATUS_CREATED or \
                                   mailing.status == Mailing.STATUS_STARTED) and \
                                  timezone.now() < mailing.end_time
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = Mailing.STATUS_CREATED
        messages.success(self.request, "Рассылка успешно создана!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при создании рассылки. Проверьте введенные данные.")
        return super().form_invalid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

    def form_valid(self, form):
        if self.object.status == Mailing.STATUS_COMPLETED:
            messages.error(self.request, "Завершенную рассылку нельзя редактировать.")
            return redirect('mailing:mailing_detail', pk=self.object.pk)

        messages.success(self.request, "Рассылка успешно обновлена!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при обновлении рассылки. Проверьте введенные данные.")
        return super().form_invalid(form)


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Рассылка успешно удалена!")
        return super().form_valid(form)


class MailingSendView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = Mailing

    def test_func(self):
        mailing_pk = self.kwargs['pk']
        mailing = get_object_or_404(Mailing, pk=mailing_pk)
        return mailing.owner == self.request.user

    def post(self, request, pk, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=pk)

        if timezone.now() >= mailing.end_time:
            messages.error(request, "Рассылка не может быть отправлена, так как ее время окончания уже наступило.")
            return redirect('mailing:mailing_detail', pk=pk)

        if mailing.status == Mailing.STATUS_COMPLETED:
            messages.error(request, "Завершенную рассылку нельзя отправить.")
            return redirect('mailing:mailing_detail', pk=pk)

        successful, failed = send_single_mailing(mailing)

        if successful > 0:
            messages.success(request,
                             f"Рассылка '{mailing.message.subject}' успешно отправлена {successful} получателям. Неудачных: {failed}.")
        else:
            messages.warning(request,
                             f"Рассылка '{mailing.message.subject}' не была отправлена ни одному получателю. Ошибок: {failed}.")

        return redirect('mailing:mailing_detail', pk=pk)


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailing/mailing_attempt_list.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модератор продуктов').exists():
            return MailingAttempt.objects.all().order_by('-attempt_time')
        return MailingAttempt.objects.filter(mailing__owner=self.request.user).order_by('-attempt_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = self.get_queryset()

        context['total_attempts'] = queryset.count()
        context['successful_attempts'] = queryset.filter(status=MailingAttempt.STATUS_SUCCESS).count()
        context['failed_attempts'] = queryset.filter(status=MailingAttempt.STATUS_FAILED).count()

        context['total_sent_messages'] = context['successful_attempts']

        if self.request.user.groups.filter(name='Модератор продуктов').exists():
            context['total_mailings_for_stats'] = Mailing.objects.count()
            context['active_mailings_for_stats'] = Mailing.objects.filter(status=Mailing.STATUS_STARTED).count()
            context['unique_recipients_for_stats'] = Client.objects.count()
        else:
            context['total_mailings_for_stats'] = Mailing.objects.filter(owner=self.request.user).count()
            context['active_mailings_for_stats'] = Mailing.objects.filter(owner=self.request.user,
                                                                          status=Mailing.STATUS_STARTED).count()

            user_mailings = Mailing.objects.filter(owner=self.request.user)
            unique_recipients_ids = set()
            for mailing in user_mailings:
                for recipient in mailing.recipients.all():
                    unique_recipients_ids.add(recipient.pk)
            context['unique_recipients_for_stats'] = len(unique_recipients_ids)

        return context


class MailingToggleActiveView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Представление для включения/отключения рассылки (только для менеджеров).
    Менеджер может перевести рассылку в статус 'Приостановлена' (если она 'Создана' или 'Запущена'),
    и обратно из 'Приостановлена' в 'Создана'.
    """

    def test_func(self):
        return self.request.user.has_perm('mailing.can_deactivate_mailings')

    def post(self, request, pk, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=pk)

        if mailing.status == Mailing.STATUS_COMPLETED:
            messages.error(request, "Завершенную рассылку нельзя отключить или включить.")
            return redirect('mailing:mailing_detail', pk=pk)

        if mailing.status == Mailing.STATUS_PAUSED:
            mailing.status = Mailing.STATUS_CREATED
            messages.success(request, f"Рассылка '{mailing.message.subject}' успешно включена (статус 'Создана').")
        else:
            mailing.status = Mailing.STATUS_PAUSED
            messages.warning(request, f"Рассылка '{mailing.message.subject}' успешно приостановлена.")

        mailing.save()
        return redirect('mailing:mailing_detail', pk=pk)