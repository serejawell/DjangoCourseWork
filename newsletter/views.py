from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from newsletter.forms import NewsletterForm, ClientForm, NewsletterManagerForm
from newsletter.models import Client, Message, Newsletter


def index_view(request):
    '''Базовый приветственный шаблон сайта'''
    return render(request, 'newsletter/base_welcome.html')


class PersonalAccountOverviewView(TemplateView):
    '''Шаблон персонального аккаунта пользователя'''
    template_name = 'newsletter/personal_account_overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_list'] = Client.objects.all()  # Список клиентов
        context['newsletter_list'] = Newsletter.objects.all()  # Список рассылок
        context['message_list'] = Message.objects.all()  # Список рассылок
        return context


# CLIENT

class ClientListView(LoginRequiredMixin, ListView):
    '''Контроллер вывода списка клиентов'''
    model = Client

    def get_queryset(self):
        '''Возвращает список клиентов текущего пользователя, отсортированный по дате добавления'''
        return Client.objects.filter(user=self.request.user).order_by('-created_at')


class ClientDetailView(LoginRequiredMixin, DetailView):
    '''Контроллер просмотра клиента'''
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    '''Контроллер создания клиента'''
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')

    def form_valid(self, form):
        '''Привязываем клиента к пользователю'''
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    '''Контроллер обновления информации о клиенте'''
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    '''Контроллер удаления клиента'''
    model = Client
    success_url = reverse_lazy('newsletter:client_list')


# NEWSLETTER


class NewsletterListView(LoginRequiredMixin, ListView):
    '''Контроллер просмотра рассылок'''
    model = Newsletter

    def get_queryset(self):
        return Newsletter.objects.filter(user=self.request.user)


class NewsletterAllListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    '''Контроллер просмотра рассылок'''
    model = Newsletter
    permission_required = 'newsletter.can_change_newsletter_status'
    def get_queryset(self):
        return Newsletter.objects.all()


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    '''Контроллер создания рассылок'''
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter:newsletter_list')

    def get_context_data(self, **kwargs):
        '''При создании рассылки показывает только клиентов пользователя'''
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.filter(user=self.request.user)
        return context

    def get_form_kwargs(self):
        '''Передаем текущего пользователя в форму'''
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Добавляем текущего пользователя
        return kwargs

    def form_valid(self, form):
        '''Привязываем рассылку к пользователю'''
        form.instance.user = self.request.user
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    '''Контроллер обновления информации о рассылке'''
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter:newsletter_list')

    def get_form_class(self):
        '''Возвращаем форму на основе прав пользователя'''
        if self.request.user == self.get_object().user:
            return self.form_class
        elif self.request.user.has_perm('newsletter.set_published'):
            return NewsletterManagerForm
        else:
            raise PermissionDenied



class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    '''Контроллер удаления рассылок'''
    model = Newsletter
    success_url = reverse_lazy('newsletter:newsletter_list')


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    '''Контроллер просмотра информации о рассылке'''
    model = Newsletter


# MESSAGE

class MessageListView(LoginRequiredMixin, ListView):
    '''Контроллер просмотра сообщений'''
    model = Message

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    '''Контроллер просмотра информации о сообщении'''
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    '''Контроллер создания сообщения'''
    model = Message
    fields = ('title', 'message')
    success_url = reverse_lazy('newsletter:message_list')

    def form_valid(self, form):
        '''Привязываем сообщение к пользователю'''
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    '''Контроллер обновления сообщения'''
    model = Message
    fields = ('title', 'message',)
    success_url = reverse_lazy('newsletter:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    '''Контроллер удаления сообщения'''
    model = Message
    success_url = reverse_lazy('newsletter:message_list')
