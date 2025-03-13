from django.urls import path
from .views import HomeView, ProductDetailView, AddProductView, ContactsView, ProductListView

app_name = 'catalog'  # Убедитесь, что пространство имен задано

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Главная страница
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # Подробности о товаре
    path('add/', AddProductView.as_view(), name='add_product'),  # URL для добавления товара
    path('contacts/', ContactsView.as_view(), name='contacts'),  # Контакты
    path('list/', ProductListView.as_view(), name='product_list'),  # URL для списка товаров
]