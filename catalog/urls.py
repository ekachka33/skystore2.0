from django.urls import path
from .views import ProductDetailView, AddProductView, ContactsView, ProductListView

app_name = 'catalog'  # Убедитесь, что пространство имен задано

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),  # Главная страница - список продуктов
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # Подробности о товаре
    path('add/', AddProductView.as_view(), name='add_product'),  # URL для добавления товара
    path('contacts/', ContactsView.as_view(), name='contacts'),  # Контакты
]