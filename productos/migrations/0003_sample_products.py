from django.db import migrations


def crear_productos_ejemplo(apps, schema_editor):
    Producto = apps.get_model('productos', 'Producto')
    productos = [
        {
            'nombre': 'Auriculares Gamer',
            'codigo': 'PROD-0001',
            'descripcion': 'Auriculares con micrófono, sonido estéreo y luces RGB.',
            'precio': '59.99',
            'cantidad': 12,
            'stock_minimo': 5,
            'estado': True,
        },
        {
            'nombre': 'Teclado Mecánico',
            'codigo': 'PROD-0002',
            'descripcion': 'Teclado mecánico con switches azules y retroiluminación.',
            'precio': '89.90',
            'cantidad': 3,
            'stock_minimo': 5,
            'estado': True,
        },
        {
            'nombre': 'Mouse Óptico',
            'codigo': 'PROD-0003',
            'descripcion': 'Mouse ergonómico con sensor de alta precisión.',
            'precio': '39.50',
            'cantidad': 0,
            'stock_minimo': 2,
            'estado': True,
        },
    ]
    for producto in productos:
        Producto.objects.update_or_create(codigo=producto['codigo'], defaults=producto)


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_alter_producto_cantidad_alter_producto_nombre_and_more'),
    ]

    operations = [
        migrations.RunPython(crear_productos_ejemplo),
    ]
