# catalog/services.py

from django.core.cache import cache # Импортируем кеш для низкоуровневого кеширования
from catalog.models import Product, Category # Импортируем модели

def get_products_by_category(category_pk):
    """
    Сервисная функция, возвращающая список продуктов по указанной категории.
    Использует низкоуровневое кеширование.
    """
    if not category_pk:
        return Product.objects.all() # Если категория не указана, возвращаем все продукты

    # Генерируем ключ кеша. Важно, чтобы ключ был уникальным для каждой категории.
    cache_key = f'products_by_category_{category_pk}'

    # Пытаемся получить данные из кеша
    products = cache.get(cache_key)

    if products is None:
        # Если данных нет в кеше, получаем их из базы данных
        try:
            category = Category.objects.get(pk=category_pk)
            products = Product.objects.filter(category=category)

            cache.set(cache_key, products, 300)
            print(f"Products for category {category_pk} fetched from DB and cached.") # Для отладки
        except Category.DoesNotExist:
            products = Product.objects.none() # Если категория не найдена, возвращаем пустой QuerySet
            print(f"Category {category_pk} not found. Returning empty queryset.") # Для отладки
    else:
        print(f"Products for category {category_pk} fetched from cache.") # Для отладки

    return products