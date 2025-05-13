from django.urls import path
from . import views

urlpatterns = [
    path('buscar/', views.buscar_cliente_view, name='buscar_cliente'),
    path('api/cliente/', views.consultar_cliente_api, name='consultar_cliente_api'),
    path('exportar/excel/', views.exportar_cliente_excel, name='exportar_cliente_excel'),
    path('api/generar_reporte_fidelizacion/', views.generar_reporte_fidelizacion, name='generar_reporte_fidelizacion'),
]
