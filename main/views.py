from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView

from main.forms import ClientAddForm
from main.models import Client


class IndexView(TemplateView):
    template_name = 'main/base.html'
    extra_context = {'title': "Главная страница"}


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


class ClientDetailtView(LoginRequiredMixin, DetailView):
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
