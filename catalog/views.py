from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import Product
from .forms import ProductForm
from django.urls import reverse_lazy

class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'latest_products'

    def get_queryset(self):
        return Product.objects.order_by('-created_at')[:5]  # Получаем последние 5 продуктов

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        # Здесь можно добавить сохранение данных в БД или отправку email

        # Сообщение об успешной отправке
        messages.success(request, f"Спасибо, {name}! Ваше сообщение отправлено.")
        return redirect('catalog:contacts')  # Перенаправление на страницу контактов

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class AddProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:product_list')  # Перенаправление на список товаров

    def form_valid(self, form):
        messages.success(self.request, "Товар успешно добавлен!")  # Сообщение об успешном добавлении
        return super().form_valid(form)

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        return Product.objects.all()