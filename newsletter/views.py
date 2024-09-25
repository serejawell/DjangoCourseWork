from django.shortcuts import render

from django.views.generic import CreateView, ListView,DetailView,UpdateView,DeleteView
from newsletter.models import User,Client,Message,Company,Newsletter

def base_view(request):
    return render(request, 'base.html')