from django.urls import path
from .views import home, product_detail, add_product, contacts, product_list

app_name = 'catalog'  # Убедитесь, что пространство имен задано

urlpatterns = [
    path('', home, name='home'),  # Главная страница
    path('product/<int:pk>/', product_detail, name='product_detail'),  # Подробности о товаре
    path('add/', add_product, name='add_product'),  # URL для добавления товара
    path('contacts/', contacts, name='contacts'),  # Контакты
    path('list/', product_list, name='product_list'),  # URL для списка товаров
]