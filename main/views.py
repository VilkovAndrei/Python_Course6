import random
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Post
from main.forms import ClientAddForm, MessageAddForm, MallingAddForm
from main.models import Client, MessageMailing, Mailing, AttemptMailing


class IndexView(TemplateView):
    template_name = 'main/home.html'
    extra_context = {'title': "Главная страница"}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailing_count'] = Mailing.objects.all().count()
        context_data['active_mailing_count'] = Mailing.objects.filter(status_mailing='Запущена').count()
        post_list = list(Post.objects.filter(is_published=True))
        random.shuffle(post_list)
        context_data['object_list'] = post_list[:3]
        context_data['clients_count'] = Client.objects.all().count()
        context_data['title'] = 'Главная'
        return context_data


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientAddForm
    success_url = reverse_lazy('main:client_list')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['title'] = 'Добавление клиента'

        return context_data

    def form_valid(self, form):
        client = form.save()
        client.owner = self.request.user
        client.save()

        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "main/client_list.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['object_list'] = Client.objects.filter(owner=self.request.user)

        # context_data['object_groups_user'] = str(self.request.user.groups.filter(name='manager'))
        # context_data['object_groups'] = '<QuerySet [<Group: manager>]>'

        context_data['title'] = 'Клиенты'

        return context_data


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['title'] = 'Просмотр клиента'

        return context_data


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientAddForm

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['title'] = 'Редактирование клиента'

        return context_data

    def test_func(self):
        if self.get_object().owner == self.request.user or self.request.user.is_superuser:
            return True

        else:
            return self.handle_no_permission()

    def get_success_url(self):
        return reverse('main:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('main:client_list')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['title'] = 'Удаление клиента'

        return context_data


class MessageMailingCreateView(LoginRequiredMixin, CreateView):
    model = MessageMailing
    form_class = MessageAddForm
    template_name = "main/message_mailing_form.html"
    success_url = reverse_lazy('main:message_list')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['title'] = 'Добавление сообщения'

        return context_data

    def form_valid(self, form):
        result = form.save()
        result.owner = self.request.user
        result.save()

        return super().form_valid(form)


class MessageMailingListView(LoginRequiredMixin, ListView):
    model = MessageMailing
    template_name = "main/message_mailing_list.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        message = MessageMailing.objects.filter(owner=self.request.user)

        # context_data['object_groups_user'] = str(self.request.user.groups.filter(name='manager'))
        # context_data['object_groups'] = '<QuerySet [<Group: manager>]>'
        context_data['object_list'] = message
        context_data['title'] = 'Сообщения'

        return context_data


class MessageMailingDetailView(LoginRequiredMixin, DetailView):
    model = MessageMailing
    template_name = "main/message_mailing_detail.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['title'] = 'Просмотр сообщения'

        return context_data


class MessageMailingUpdateView(LoginRequiredMixin, UpdateView):
    model = MessageMailing
    form_class = MessageAddForm
    template_name = "main/message_mailing_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['title'] = 'Редактирование сообщения'

        return context_data

    def get_success_url(self):
        return reverse('main:message_detail', args=[self.kwargs.get('pk')])


class MessageMailingDeleteView(LoginRequiredMixin, DeleteView):
    model = MessageMailing
    success_url = reverse_lazy('main:message_list')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['title'] = 'Удаление сообщения'

        return context_data


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MallingAddForm
    success_url = reverse_lazy('main:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        # kwargs.update({'request': self.request})
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['title'] = 'Добавление рассылки'
        context_data['form'].request = self.request

        return context_data

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        queryset = queryset.filter(owner=user)
        return queryset


    def form_valid(self, form):
        result = form.save()
        result.owner = self.request.user
        result.save()

        return super().form_valid(form)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "main/mailing_list.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        if self.request.user.groups.filter(name='mailing_manager') or self.request.user.is_superuser:
            mailing = Mailing.objects.all()
            context_data['user_is_manager'] = True
        else:
            mailing = Mailing.objects.filter(owner=self.request.user)

        # context_data['object_groups_user'] = str(self.request.user.groups.filter(name='manager'))
        # context_data['object_groups'] = '<QuerySet [<Group: manager>]>'
        context_data['object_list'] = mailing
        context_data['title'] = 'Рассылки'

        return context_data


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        mailing = Mailing.objects.all()

        for mailing_clients in mailing:
            context_data['object_client'] = mailing_clients.clients.all()

        context_data['title'] = 'Просмотр рассылки'

        return context_data


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MallingAddForm

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        queryset = queryset.filter(owner=user)
        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        # kwargs.update({'request': self.request})
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['title'] = 'Редактирование рассылки'

        return context_data

    def get_success_url(self):
        return reverse('main:mailing_detail', args=[self.kwargs.get('pk')])


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('main:mailing_list')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['title'] = 'Удаление рассылки'

        return context_data

def blocked_the_mailing(request, pk):
    """Блокирует или снимает блокировку с рассылки"""
    mailing_item = get_object_or_404(Mailing, pk=pk)
    if mailing_item.is_active:
        mailing_item.is_active = False
    elif not mailing_item.is_active:
        mailing_item.is_active = True
    mailing_item.save()
    return redirect(reverse('main:mailing_list'))

def close_or_start_the_mailing(request, pk):
    """Завершает или запускает рассылку"""
    mailing_item = get_object_or_404(Mailing, pk=pk)
    if mailing_item.status_mailing == "Запущена":
        mailing_item.status_mailing = "Завершена"
    elif mailing_item.status_mailing == "Завершена":
        mailing_item.status_mailing = "Запущена"
    mailing_item.save()
    return redirect(reverse('main:mailing_list'))


class ReportListView(LoginRequiredMixin, ListView):
    model = AttemptMailing
    template_name = "main/report.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        if self.request.user.is_superuser:
            report_list = AttemptMailing.objects.all()
        else:
            report_list = AttemptMailing.objects.filter(mailing__owner=self.request.user)

        context_data['object_list'] = report_list
        context_data['title'] = 'Отчет'

        return context_data
