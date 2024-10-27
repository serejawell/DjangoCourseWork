from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from newsletter.forms import NewsletterForm, ClientForm
from newsletter.models import Client, Message, Newsletter


def index_view(request):
    return render(request, 'newsletter/base_welcome.html')


class PersonalAccountOverviewView(TemplateView):
    template_name = 'newsletter/personal_account_overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_list'] = Client.objects.all()  # Список клиентов
        context['newsletter_list'] = Newsletter.objects.all()  # Список рассылок
        context['message_list'] = Message.objects.all()  # Список рассылок
        return context


# CLIENT

class ClientListView(ListView):
    model = Client

class ClientDetailView(DetailView):
    model = Client

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:personal_account_overview')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:personal_account_overview')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('newsletter:personal_account_overview')


# NEWSLETTER


class NewsletterListView(ListView):
    model = Newsletter


class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter:personal_account_overview')


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter:personal_account_overview')


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy('newsletter:personal_account_overview')


class NewsletterDetailView(DetailView):
    model = Newsletter


# MESSAGE

class MessageListView(ListView):
    model = Message

class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    fields = ('title', 'message')
    success_url = reverse_lazy('newsletter:personal_account_overview')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('title', 'message',)
    success_url = reverse_lazy('newsletter:personal_account_overview')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('newsletter:personal_account_overview')
