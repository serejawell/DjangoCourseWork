from django.urls import path
from newsletter.apps import NewsletterConfig
from newsletter.views import index_view, ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    NewsletterListView, PersonalAccountOverviewView, MessageCreateView, MessageDeleteView, MessageUpdateView, \
    NewsletterCreateView, NewsletterDeleteView, NewsletterUpdateView, NewsletterDetailView

app_name = NewsletterConfig.name

urlpatterns = [
    path('', index_view, name='base'),
    path('personal_account/', PersonalAccountOverviewView.as_view(), name='personal_account_overview'),
    path('personal_account/create_client', ClientCreateView.as_view(), name='client_create'),
    path('personal_account/update_client/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('personal_account/delete_client/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('personal_account/create_message/', MessageCreateView.as_view(), name='message_create'),
    path('personal_account/update_message/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('personal_account/delete_message/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('personal_account/', NewsletterListView.as_view(), name='newsletter_list'),
    path('personal_account/newsletter_create', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('personal_account/update_newsletter/<int:pk>', NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('personal_account/delete_newsletter/<int:pk>', NewsletterDeleteView.as_view(), name='newsletter_delete'),
    path('personal_account/newsletter/<int:pk>', NewsletterDetailView.as_view(), name='newsletter_detail'),

]
