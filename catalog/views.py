# catalog/views.py

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View # <--- Добавляем View для ProductUnpublishView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin # <--- Добавляем PermissionRequiredMixin

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
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Товар успешно добавлен!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при добавлении товара. Пожалуйста, проверьте введенные данные.")
        return super().form_invalid(form)


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        return Product.objects.all()

# --- Представления, требующие авторизации и прав ---

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Товар успешно обновлен!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при обновлении товара. Проверьте данные.")
        return super().form_invalid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        # Удалить продукт может владелец ИЛИ пользователь с правом на удаление (модератор)
        return obj.owner == user or user.has_perm('catalog.delete_product')


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View): # <--- НОВОЕ ПРЕДСТАВЛЕНИЕ для отмены публикации
    model = Product
    permission_required = 'catalog.can_unpublish_product' # Требуемое разрешение
    # Можно добавить raise_exception=True для 403 ошибки вместо перенаправления на логин

    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        if product.is_published:
            product.is_published = False
            product.save()
            messages.success(request, f"Продукт '{product.name}' успешно снят с публикации.")
        else:
            messages.info(request, f"Продукт '{product.name}' уже не опубликован.")
        return redirect('catalog:product_detail', pk=pk)
        # Если захочешь перенаправить на список: return redirect('catalog:product_list')