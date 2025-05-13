from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Para redirigir la raíz

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirigir de la raíz (/) a /buscar/
    path('', RedirectView.as_view(url='/buscar/', permanent=False)),

    # Cargar las URLs de la app core
    path('', include('core.urls')),
]