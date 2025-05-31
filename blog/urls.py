from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('<int:pk>/edit/', BlogUpdateView.as_view(), name='blog_update'),
]