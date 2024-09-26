from newsletter.models import User, Client, Message,  Newsletter
from newsletter.models import Newsletter
from django.urls import path
from newsletter.apps import NewsletterConfig
from newsletter.views import index_view, ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    NewsletterListView, PersonalAccountOverviewView

app_name = NewsletterConfig.name

urlpatterns = [
    path('', index_view, name='base'),
    path('personal_account/create', ClientCreateView.as_view(), name='client_create'),
    path('personal_account/', PersonalAccountOverviewView.as_view(), name='personal_account_overview'),
    path('personal_account/update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('personal_account/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('personal_account/', NewsletterListView.as_view(), name='newsletter_list'),

]
