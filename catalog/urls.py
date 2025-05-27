# catalog/urls.py

from django.urls import path
from .views import HomeView, ContactsView, ProductListView, ProductDetailView, AddProductView, ProductUpdateView, ProductDeleteView, ProductUnpublishView # <--- Импортируем ProductUnpublishView

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('home/', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('add/', AddProductView.as_view(), name='add_product'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('<int:pk>/unpublish/', ProductUnpublishView.as_view(), name='unpublish_product'), # <--- НОВЫЙ URL ДЛЯ ОТМЕНЫ ПУБЛИКАЦИИ
]