# catalog/admin.py

from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_published', 'owner', 'created_at')
    list_filter = ('category', 'is_published', 'owner')
    search_fields = ('name', 'description')
    list_editable = ('is_published',)

