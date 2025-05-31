from django.core.management.base import BaseCommand
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Добавить тестовые продукты в базу данных'

    def handle(self, *args, **kwargs):
        # Очистите существующие данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создайте тестовые категории
        category = Category.objects.create(name='Тестовая категория', description='Категория для тестирования')

        # Создайте тестовые продукты
        Product.objects.create(name='Тестовый продукт 1', description='Описание тестового продукта 1', category=category, price=10.00)
        Product.objects.create(name='Тестовый продукт 2', description='Описание тестового продукта 2', category=category, price=20.00)
        Product.objects.create(name='Тестовый продукт 3', description='Описание тестового продукта 3', category=category, price=30.00)
        Product.objects.create(name='Тестовый продукт 4', description='Описание тестового продукта 4', category=category, price=40.00)
        Product.objects.create(name='Тестовый продукт 5', description='Описание тестового продукта 5', category=category, price=50.00)

        self.stdout.write(self.style.SUCCESS('Успешно добавлены тестовые продукты'))