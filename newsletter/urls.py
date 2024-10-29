from django.urls import path
from newsletter.apps import NewsletterConfig
from newsletter.views import HomePageView, ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    NewsletterListView, PersonalAccountOverviewView, MessageCreateView, MessageDeleteView, MessageUpdateView, \
    NewsletterCreateView, NewsletterDeleteView, NewsletterUpdateView, NewsletterDetailView, MessageDetailView, \
    ClientDetailView, MessageListView, NewsletterAllListView
from users.functions import toggle_newsletter_status

app_name = NewsletterConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='base'),
    path('account/', PersonalAccountOverviewView.as_view(), name='personal_account_overview'),

    path('account/clients', ClientListView.as_view(), name='client_list'),
    path('account/create_client', ClientCreateView.as_view(), name='client_create'),
    path('account/client/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('account/update_client/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('account/delete_client/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    # MESSAGES
    path('account/messages/', MessageListView.as_view(), name='message_list'),
    path('account/create_message/', MessageCreateView.as_view(), name='message_create'),
    path('account/message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('account/update_message/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('account/delete_message/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    # NEWSLETTER
    path('account/newsletters', NewsletterListView.as_view(), name='newsletter_list'),
    path('account/newsletters_all',
         NewsletterAllListView.as_view(template_name='newsletter/newsletter_admin_list.html'),
         name='newsletter_list_all'),
    path('personal_account/newsletter_create', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('personal_account/update_newsletter/<int:pk>', NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('personal_account/delete_newsletter/<int:pk>', NewsletterDeleteView.as_view(), name='newsletter_delete'),
    path('personal_account/newsletter/<int:pk>', NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('personal_account/newsletter/toggle_status/<int:newsletter_id>/', toggle_newsletter_status, name='toggle_newsletter_status'),

]
