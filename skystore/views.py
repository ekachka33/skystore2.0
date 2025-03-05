from django.contrib import messages
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


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
