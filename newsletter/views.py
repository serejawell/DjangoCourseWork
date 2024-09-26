from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from newsletter.models import User, Client, Message, Newsletter


def index_view(request):
    return render(request, 'base.html')

class PersonalAccountOverviewView(TemplateView):
    template_name = 'newsletter/personal_account_overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Client.objects.all()  # Список клиентов
        context['newsletter_list'] = Newsletter.objects.all()  # Список рассылок
        return context


class NewsletterListView(ListView):
    model = Newsletter



class ClientListView(ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = ('last_name', 'first_name', 'middle_name', 'email')
    success_url = reverse_lazy('newsletter:personal_account_overview')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('last_name', 'first_name', 'middle_name', 'email')
    success_url = reverse_lazy('newsletter:personal_account_overview')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('newsletter:personal_account_overview')
