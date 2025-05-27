# catalog/models.py

from django.db import models
from django.urls import reverse
from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **{'null': True, 'blank': True})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **{'null': True, 'blank': True})
    image = models.ImageField(upload_to='products/', verbose_name='Изображение (превью)', **{'null': True, 'blank': True})
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')


    is_published = models.BooleanField(default=False, verbose_name='Опубликован')

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.category})"


    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']

        permissions = [
            ("can_unpublish_product", "Can unpublish product"),

        ]