from newsletter.models import User, Client, Message, Company, Newsletter
from newsletter.models import Newsletter
from django.urls import path
from newsletter.apps import NewsletterConfig
from newsletter.views import base_view

app_name = NewsletterConfig.name

urlpatterns = [
    path('', base_view, name='base')
]
