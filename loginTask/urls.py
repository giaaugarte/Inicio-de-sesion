from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

# Lista de patrones de URL para la aplicación
urlpatterns = [
    # Ruta para redirigir a "accounts/" en la URL raíz
    path(
        "",
        RedirectView.as_view(url="accounts/", permanent=False),
        name="index"
    ),

    # Ruta para el panel de administración de Django
    path('admin/', admin.site.urls),

    # Ruta para incluir las URLs del aplicativo "tasks"
    path('tasks/', include('tasks.urls')),

    # Ruta para incluir las URLs del aplicativo "accounts"
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
