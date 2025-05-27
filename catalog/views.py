# catalog/views.py

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Product, Category # <--- Импортируем Category, если нужна для контекста
from .forms import ProductForm
from .services import get_products_by_category # <--- Импортируем нашу сервисную функцию


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


@method_decorator(cache_page(60 * 5), name='dispatch')
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

    def get_context_data(self, **kwargs): # <--- ДОБАВЬ ЭТОТ МЕТОД
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all() # Передаем список всех категорий
        return context



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
        return obj.owner == user or user.has_perm('catalog.delete_product')


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = Product
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        if product.is_published:
            product.is_published = False
            product.save()
            messages.success(request, f"Продукт '{product.name}' успешно снят с публикации.")
        else:
            messages.info(request, f"Продукт '{product.name}' уже не опубликован.")
        return redirect('catalog:product_detail', pk=pk)


class ProductByCategoryListView(ListView): # <--- НОВОЕ ПРЕДСТАВЛЕНИЕ!
    """
    Представление для отображения продуктов по выбранной категории.
    """
    model = Product
    template_name = 'catalog/products_by_category.html' # Новый шаблон
    context_object_name = 'products' # Имя переменной в шаблоне

    def get_queryset(self):
        category_pk = self.kwargs['pk'] # Получаем pk категории из URL
        # Используем нашу сервисную функцию
        queryset = get_products_by_category(category_pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем объект категории в контекст для отображения заголовка
        category_pk = self.kwargs['pk']
        try:
            context['category'] = Category.objects.get(pk=category_pk)
        except Category.DoesNotExist:
            context['category'] = None # Если категория не найдена
        context['categories'] = Category.objects.all() # Все категории для навигации
        return context