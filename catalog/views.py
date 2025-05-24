from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin # <--- Эту строку нужно добавить!

from .models import Product
from .forms import ProductForm


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'latest_products'

    def get_queryset(self):
        return Product.objects.order_by('-created_at')[:5]


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        messages.success(request, f"Спасибо, {name}! Ваше сообщение отправлено.")
        return redirect('catalog:contacts')


class ProductDetailView(DetailView):
    # Если на этой странице нет действий по изменению данных, то она может быть общедоступной.
    # Если на ней есть кнопки "Редактировать", "Удалить" и т.п., то логично ее тоже защитить.
    # Для целей задания, пока оставим её общедоступной, как "просмотр деталей"
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class AddProductView(LoginRequiredMixin, CreateView): # <--- ВОТ ЗДЕСЬ ДОБАВЬ LoginRequiredMixin!
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        messages.success(self.request, "Товар успешно добавлен!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при добавлении товара. Пожалуйста, проверьте введенные данные.")
        return super().form_invalid(form)

class ProductListView(ListView): # Это представление остается общедоступным
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        return Product.objects.all()