from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render
from .models import Product

def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]  # Получаем последние 5 продуктов
    return render(request, 'home.html', {'latest_products': latest_products})

def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        # Тут можно добавить сохранение данных в БД или отправку email

        # Сообщение об успешной отправке
        messages.success(request, f"Спасибо, {name}! Ваше сообщение отправлено.")
        # Вы можете добавить редирект, чтобы избежать повторной отправки формы при обновлении страницы
        return render(request, "contacts.html")

    return render(request, "contacts.html")
