from django.urls import path
from django.views.decorators.cache import cache_page

from main.apps import MainConfig
from main.views import IndexView, MessageMailingCreateView, MessageMailingListView, MessageMailingDetailView, \
    MessageMailingUpdateView, MessageMailingDeleteView, MailingListView, MailingCreateView, MailingDetailView, \
    MailingUpdateView, MailingDeleteView, ReportListView, close_or_start_the_mailing

from main.views import ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, ClientDeleteView

app_name = MainConfig.name


urlpatterns = [
    # path('', HomeListView.as_view(), name='home_list'),
    path('', IndexView.as_view(), name='home'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('add_client/', ClientCreateView.as_view(), name='create_client'),
    path('view_client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('update_client/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
    path('message_list/', MessageMailingListView.as_view(), name='message_list'),
    path('create_message/', MessageMailingCreateView.as_view(), name='create_message'),
    path('view_message/<int:pk>/', MessageMailingDetailView.as_view(), name='message_detail'),
    path('update_message/<int:pk>', MessageMailingUpdateView.as_view(), name='update_message'),
    path('delete_message/<int:pk>', MessageMailingDeleteView.as_view(), name='delete_message'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('view_mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('update_mailing/<int:pk>', MailingUpdateView.as_view(), name='update_mailing'),
    path('delete_mailing/<int:pk>', MailingDeleteView.as_view(), name='delete_mailing'),
    path('activity/<int:pk>', close_or_start_the_mailing, name='close_or_start_the_mailing'),
    path('report/', ReportListView.as_view(), name='report'),
]
