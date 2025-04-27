from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    search_fields = ('name', 'description')

    def save_model(self, request, obj, form, change):
        # Убедитесь, что валидация выполняется в форме, а не здесь
        super().save_model(request, obj, form, change)

admin.site.register(Product, ProductAdmin)