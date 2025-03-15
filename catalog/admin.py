from django.contrib import admin
from .models import Product, Category, Contact


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')

    def save_model(self, request, obj, form, change):
        # Проверка на запрещенные слова в имени и описании
        forbidden_words = [
            'казино', 'криптовалюта', 'крипта',
            'биржа', 'дешево', 'бесплатно',
            'обман', 'полиция', 'радар'
        ]
        # Проверка имени
        if any(word in obj.name.lower() for word in forbidden_words):
            raise ValueError("Имя продукта содержит запрещенные слова.")
        # Проверка описания
        if any(word in obj.description.lower() for word in forbidden_words):
            raise ValueError("Описание продукта содержит запрещенные слова.")

        super().save_model(request, obj, form, change)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact)