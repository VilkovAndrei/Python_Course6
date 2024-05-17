from django.urls import path
from django.views.decorators.cache import cache_page

from main.apps import MainConfig
from main.views import IndexView

# from main.views import (ClientListView, ClientCreateView, ClientDetailtView, ClientUpdateView, ClientDeleteView,
#                         MessageListView, MessageCreateView, MessageDetailtView, MessageUpdateView, MessageDeleteView,
#                         MailingListView, MailingCreateView, MailingDetailtView, MailingUpdateView, MailingDeleteView,
#                         disable_the_mailing, ReportListView, HomeListView)

app_name = MainConfig.name


urlpatterns = [
    # path('', HomeListView.as_view(), name='home_list'),
    path('', IndexView.as_view(), name='home'),
]