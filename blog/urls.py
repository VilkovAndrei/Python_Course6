from django.urls import path
from django.views.decorators.cache import never_cache

from blog.views import PostListView, PostCreateView, PostUpdateView, PostDetailView, PostDeleteView

app_name = 'blog'


urlpatterns = [
    path('post_list/', never_cache(PostListView.as_view()), name='post_list'),
    path('post_detail/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post_create/', never_cache(PostCreateView.as_view()), name='post_create'),
    path('post_update/<int:pk>', never_cache(PostUpdateView.as_view()), name='post_update'),
    path('post_delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
]
