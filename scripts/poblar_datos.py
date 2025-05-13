from django.utils import timezone
from decimal import Decimal
from core.models import TipoDocumento, Cliente, Producto, Compra
import datetime

def run():
    # Borrar datos anteriores
    Compra.objects.all().delete()
    Cliente.objects.all().delete()
    Producto.objects.all().delete()
    TipoDocumento.objects.all().delete()

    # Crear tipo de documento
    tipo_documento_cedula = TipoDocumento.objects.create(nombre='Cédula')

    # Crear productos con precios más altos
    producto1 = Producto.objects.create(nombre='Botella 500ml', precio=Decimal('50000'))
    producto2 = Producto.objects.create(nombre='Paquete 6 botellas', precio=Decimal('250000'))
    producto3 = Producto.objects.create(nombre='Garrafón 20L', precio=Decimal('600000'))

    documentos = ['1', '12', '123', '1234', '12345', '123456', '1234567', '12345678', '123456789']
    now = timezone.now()

    for i, doc in enumerate(documentos):
        cliente = Cliente.objects.create(
            tipo_documento=tipo_documento_cedula,
            numero_documento=doc,
            nombre=f'Cliente {i+1}',
            apellido='Prueba',
            correo=f'cliente{i+1}@mail.com',
            telefono=f'310000000{i+1}'
        )

        # Los últimos 3 clientes tendrán mayores compras para superar el umbral
        multiplicador = 3 if i >= 6 else 1

        Compra.objects.create(
            cliente=cliente,
            producto=producto1,
            cantidad=20 * multiplicador,
            precio_unitario=producto1.precio,
            fecha_compra=now - datetime.timedelta(days=10)
        )

        Compra.objects.create(
            cliente=cliente,
            producto=producto2,
            cantidad=10 * multiplicador,
            precio_unitario=producto2.precio,
            fecha_compra=now - datetime.timedelta(days=15)
        )

        Compra.objects.create(
            cliente=cliente,
            producto=producto3,
            cantidad=5 * multiplicador,
            precio_unitario=producto3.precio,
            fecha_compra=now - datetime.timedelta(days=20)
        )

        print(f"✔️ Cliente {cliente.nombre} creado con compras por un total estimado de más de {multiplicador * (20*50000 + 10*250000 + 5*600000)} COP")

    print("✅ Datos de prueba insertados correctamente.")