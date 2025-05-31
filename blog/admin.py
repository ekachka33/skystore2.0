from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published', 'view_count')
    search_fields = ('title',)
    list_filter = ('is_published',)