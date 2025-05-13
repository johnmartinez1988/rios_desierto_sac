import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .forms import BuscarClienteForm
from .models import Cliente
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta

def buscar_cliente_view(request):
    form = BuscarClienteForm()
    context = {'form': form}
    return render(request, 'core/buscar_cliente.html', context)

def consultar_cliente_api(request):
    if request.method == 'GET':
        numero_documento = request.GET.get('numero_documento')
        tipo_documento_id = request.GET.get('tipo_documento')

        if numero_documento and tipo_documento_id:
            try:
                cliente = Cliente.objects.get(numero_documento=numero_documento, tipo_documento_id=tipo_documento_id)
                cliente_data = {
                    'tipo_documento': cliente.tipo_documento.nombre,
                    'numero_documento': cliente.numero_documento,
                    'nombre': cliente.nombre,
                    'apellido': cliente.apellido,
                    'correo': cliente.correo,
                    'telefono': cliente.telefono,
                    'compras': [{'producto': compra.producto.nombre, 'fecha': compra.fecha_compra.strftime('%Y-%m-%d'), 'monto': str(compra.monto_total)} for compra in cliente.compras.all()]
                }
                return JsonResponse(cliente_data)
            except Cliente.DoesNotExist:
                return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
        else:
            return JsonResponse({'error': 'Por favor, proporcione el número y tipo de documento'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def exportar_cliente_excel(request):
    if request.method == 'GET':
        numero_documento = request.GET.get('numero_documento')
        tipo_documento_id = request.GET.get('tipo_documento')

        try:
            cliente = Cliente.objects.get(numero_documento=numero_documento, tipo_documento_id=tipo_documento_id)

            cliente_data = {
                'Tipo de Documento': [cliente.tipo_documento.nombre],
                'Número de Documento': [cliente.numero_documento],
                'Nombre': [cliente.nombre],
                'Apellido': [cliente.apellido],
                'Correo': [cliente.correo or 'N/A'],
                'Teléfono': [cliente.telefono or 'N/A'],
            }
            df_cliente = pd.DataFrame(cliente_data)

            compras_data = []
            for compra in cliente.compras.all():
                compras_data.append({
                    'Producto': compra.producto.nombre,
                    'Fecha de Compra': compra.fecha_compra.strftime('%Y-%m-%d'),
                    'Monto Total': float(compra.monto_total)
                })
            df_compras = pd.DataFrame(compras_data)

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="cliente_{cliente.numero_documento}.xlsx"'

            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df_cliente.to_excel(writer, sheet_name='Informacion Cliente', index=False)
                df_compras.to_excel(writer, sheet_name='Compras Asociadas', index=False)

            return response
        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
    return HttpResponse(status=405)

def generar_reporte_fidelizacion(request):
    hoy = timezone.now()
    fecha_limite = hoy - timedelta(days=30)

    clientes_fidelizables = Cliente.objects.annotate(
        total_compras_ultimos_30=Sum(
            'compras__monto_total',
            filter=Q(compras__fecha_compra__gte=fecha_limite)
        )
    ).filter(total_compras_ultimos_30__gte=5000000)

    data = []
    for cliente in clientes_fidelizables:
        data.append({
            'Número de Documento': cliente.numero_documento,
            'Nombre': cliente.nombre,
            'Apellido': cliente.apellido,
            'Correo': cliente.correo,
            'Teléfono': cliente.telefono,
            'Monto Total Compras (Últimos 30 días)': cliente.total_compras_ultimos_30
        })

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_fidelizacion.xlsx"'

    df.to_excel(response, index=False, sheet_name='Clientes Fidelizables')

    return response
