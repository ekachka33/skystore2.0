# catalog/services.py

from django.core.cache import cache # Импортируем кеш для низкоуровневого кеширования
from catalog.models import Product, Category # Импортируем модели

def get_products_by_category(category_pk):
    """
    Сервисная функция, возвращающая список продуктов по указанной категории.
    Использует низкоуровневое кеширование.
    """
    if not category_pk:
        return Product.objects.all()

    # Генерируем ключ кеша.
    cache_key = f'products_by_category_{category_pk}'

    products = cache.get(cache_key)

    if products is None:

        try:
            category = Category.objects.get(pk=category_pk)
            products = Product.objects.filter(category=category)

            cache.set(cache_key, products, 300)
            print(f"Products for category {category_pk} fetched from DB and cached.")
        except Category.DoesNotExist:
            products = Product.objects.none()
            print(f"Category {category_pk} not found. Returning empty queryset.")
    else:
        print(f"Products for category {category_pk} fetched from cache.")

    return products