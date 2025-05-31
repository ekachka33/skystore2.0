from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import BlogPost

class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)  # Фильтрация опубликованных статей

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        blog_post = super().get_object(queryset)
        blog_post.view_count += 1  # Увеличение счетчика просмотров
        blog_post.save()
        return blog_post

class BlogCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview_image', 'is_published']
    success_url = reverse_lazy('blog:blog_list')

class BlogUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview_image', 'is_published']
    success_url = reverse_lazy('blog:blog_list')  # Перенаправление после редактирования