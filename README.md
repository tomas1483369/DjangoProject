# Django Inventory Marketplace

Proyecto académico de inventario estilo marketplace desarrollado con Django.

## Visión general

Esta aplicación web combina gestión de productos, control de stock y carrito de compras en sesión para ofrecer una experiencia tipo marketplace.

- Autenticación y administración de usuarios.
- Catálogo de productos con filtros y búsqueda.
- Dashboard de métricas y alertas de stock.
- Carrito dinámico con soporte AJAX.
- Interfaz oscura con Bootstrap 5 local.

## Estado actual

El proyecto cuenta con dos aplicaciones principales:

- `usuarios`
- `productos`

### Funcionalidades implementadas

- Registro e inicio de sesión de usuarios.
- Dashboard con métricas clave:
  - total de usuarios
  - productos activos
  - stock bajo
  - productos agotados
- Gestión de usuarios restringida a administrador.
- CRUD de productos con imagen, cantidad, stock mínimo, código y estado.
- Catálogo con búsqueda y filtros por estado de stock.
- Detalle de producto y stock badge dinámico.
- Carrito de compras en sesión con:
  - actualización de cantidades
  - eliminación de ítems
  - vaciado completo
  - recálculo de total en tiempo real
- Carrito SPA usando Fetch API y respuesta parcial de plantilla.

### Validación y seguridad

- Validaciones de formulario y modelo para:
  - códigos de producto
  - precios positivos
  - cantidades válidas
  - contraseñas complejas
- Decoradores y servicios para administración de permisos.
- Estado de productos con banderas de stock bajo / agotado.

## Arquitectura actual

- `config/`: configuración del proyecto y URLs.
- `usuarios/`: autenticación, roles, administración y formularios.
- `productos/`: modelos, formularios, vistas de catálogo y carrito.
- `templates/`: diseño de frontend y fragmentos HTML.
- `static/`: estilos y scripts del cliente.

## Estructura de carpetas

```
DjangoProject/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── productos/
│   ├── forms.py
│   ├── managers.py
│   ├── models.py
│   ├── services.py
│   ├── urls.py
│   ├── validators.py
│   ├── views.py
│   └── migrations/
├── usuarios/
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── urls.py
│   ├── validators.py
│   ├── views.py
│   └── apps.py
├── templates/
│   ├── base.html
│   ├── catalogo.html
│   ├── dashboard.html
│   ├── producto_form.html
│   ├── registration/
│   │   ├── login.html
│   │   └── register.html
│   ├── productos/
│   │   ├── carrito.html
│   │   ├── cart_items_fragment.html
│   │   ├── catalogo_cards.html
│   │   └── producto_detalle.html
│   └── usuarios/
│       ├── lista_usuarios.html
│       └── usuario_form.html
├── static/
│   ├── css/
│   │   ├── app.css
│   │   └── bootstrap.min.css
│   └── js/
│       └── app.js
├── manage.py
└── README.md
```

## Tecnologías

- Python 3.13+
- Django 4.2.11
- SQLite
- Bootstrap 5 local
- HTML5 / CSS3
- Vanilla JavaScript
- Django Templates

## Notas importantes

- `MEDIA_URL` y `MEDIA_ROOT` están configurados para imágenes de productos.
- El carrito está basado en sesión y no incluye pasarela de pago.
- Se usa AJAX para actualizar el carrito sin recargar la página.
- La estrategia de permisos se apoya en decoradores y está lista para extenderse con `Groups`.

## Próximos pasos

1. Completar roles y permisos con `Groups`.
2. Refinar autorización con mixins y decoradores personalizados.
3. Añadir gestión de stock avanzada en el dashboard.
4. Mejorar validaciones y mensajes de usuario.
5. Integrar acciones del carrito desde la página de producto.

## Cómo ejecutar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install django pillow
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Observación

Este README refleja el estado actual del proyecto y se actualizará conforme se agreguen nuevas funcionalidades.
