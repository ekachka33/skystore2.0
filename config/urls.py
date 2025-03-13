from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls', namespace='catalog')),  # Включение маршрутов из приложения catalog
    path('blog/', include('blog.urls', namespace='blog')),  # Включение маршрутов из приложения blog
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)