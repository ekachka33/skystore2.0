from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from django.core.paginator import Paginator

def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]  # Получаем последние 5 продуктов
    return render(request, 'catalog/home.html', {'latest_products': latest_products})

def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        # Здесь можно добавить сохранение данных в БД или отправку email

        # Сообщение об успешной отправке
        messages.success(request, f"Спасибо, {name}! Ваше сообщение отправлено.")
        return redirect('catalog:contacts')  # Перенаправление на страницу контактов

    return render(request, "catalog/contacts.html")

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Получаем продукт по первичному ключу
    return render(request, 'catalog/product_detail.html', {'product': product})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Товар успешно добавлен!")  # Сообщение об успешном добавлении
            return redirect('catalog:product_list')  # Перенаправление на список товаров
    else:
        form = ProductForm()
    return render(request, 'catalog/add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 10)  # Показывать 10 товаров на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'catalog/product_list.html', {'page_obj': page_obj})