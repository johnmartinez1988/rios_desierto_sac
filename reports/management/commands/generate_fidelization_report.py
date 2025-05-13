import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Sum
from django.utils import timezone
from core.models import Cliente, Compra

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Sum, Q
from core.models import Cliente
import pandas as pd

class Command(BaseCommand):
    help = 'Generates a report of clients with total purchases over 5,000,000 COP in the last 30 days.'

    def handle(self, *args, **options):
        fecha_limite = timezone.now() - timezone.timedelta(days=30)

        # Clientes con total de compras en los últimos 30 días mayor a 5M
        clientes_fidelizar = Cliente.objects.annotate(
            total_compras=Sum(
                'compras__monto_total',
                filter=Q(compras__fecha_compra__gte=fecha_limite)
            )
        ).filter(total_compras__gt=5000000)

        data = []
        for cliente in clientes_fidelizar:
            data.append({
                'Tipo de Documento': cliente.tipo_documento.nombre,
                'Número de Documento': cliente.numero_documento,
                'Nombre': cliente.nombre,
                'Apellido': cliente.apellido,
                'Correo': cliente.correo or '',
                'Teléfono': cliente.telefono or '',
                'Monto Total Compras (últimos 30 días)': cliente.total_compras
            })

        if not data:
            self.stdout.write(self.style.WARNING("No hay clientes con compras superiores a 5'000.000 en los últimos 30 días."))
            return

        df = pd.DataFrame(data)
        nombre_archivo = f"reporte_fidelizacion_{timezone.now().strftime('%Y%m%d')}.xlsx"
        df.to_excel(nombre_archivo, index=False)

        self.stdout.write(self.style.SUCCESS(f"✅ Reporte generado correctamente: {nombre_archivo}"))
