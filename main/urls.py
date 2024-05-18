from django.urls import path
from django.views.decorators.cache import cache_page

from main.apps import MainConfig
from main.views import IndexView

from main.views import ClientListView, ClientCreateView, ClientDetailtView, ClientUpdateView, ClientDeleteView

app_name = MainConfig.name


urlpatterns = [
    # path('', HomeListView.as_view(), name='home_list'),
    path('', IndexView.as_view(), name='home'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('add_client/', ClientCreateView.as_view(), name='create_client'),
    path('view_client/<int:pk>/', ClientDetailtView.as_view(), name='client_detail'),
    path('update_client/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
]