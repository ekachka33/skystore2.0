from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='catalog/', permanent=True)),  # Перенаправление на каталог
    path('catalog/', include('catalog.urls')),  # Подключение маршрутов приложения catalog
    path('blog/', include('blog.urls')),        # Подключение маршрутов приложения blog
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)