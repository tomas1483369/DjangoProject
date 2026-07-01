# Django Inventory Marketplace

Proyecto académico de sistema de inventario estilo marketplace desarrollado con Django.

## Visión general

Este proyecto es una aplicación web de inventario con:

- Gestión de usuarios.
- Catálogo de productos.
- Carrito de compras en sesión.
- Interfaz oscura con Bootstrap local.
- Arquitectura MVT de Django.

## Estado actual

El proyecto contiene dos aplicaciones principales:

- `usuarios`
- `productos`

### Funcionalidades implementadas

- Registro de usuarios.
- Inicio y cierre de sesión.
- Dashboard después del login.
- Gestión básica de usuarios (lista, crear, editar, desactivar) restringida a superusuario.
- CRUD de productos con imagen, cantidad, stock mínimo, código y estado.
- Catálogo público de productos con búsqueda y filtros de estado.
- Detalle de producto y agregado al carrito.
- Carrito de compras en sesión con visualización de ítems, total y eliminación.
- Layout de interfaz con tema oscuro y navegación lateral.

### Arquitectura actual

Se mantiene una separación básica:

- `config/`: configuración del proyecto.
- `usuarios/`: manejo de autenticación y administración de usuarios.
- `productos/`: modelo de productos, catálogo y carrito.
- `templates/`: vistas de frontend.
- `static/`: recursos CSS y JavaScript.

También hay módulos preparados para:

- `services.py`
- `validators.py`
- `managers.py`

Estos archivos representan capas de servicio, validación y consultas personalizadas.

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

- Actualmente el proyecto usa Django 4.2.11 en `config/settings.py`.
- `MEDIA_URL` y `MEDIA_ROOT` están configurados para manejo de imágenes de productos.
- El carrito está basado en sesión y no usa pasarela de pago.
- Algunos componentes de seguridad y permisos están aplicados, pero falta completar la estrategia de roles y autorizaciones con `Groups`.

## Próximos pasos

1. Establecer roles con `Groups` y permisos finos.
2. Implementar `PermissionRequiredMixin` y decoradores personalizados.
3. Mejorar el carrito con Fetch API / AJAX para una experiencia SPA.
4. Añadir validaciones completas de modelo y formulario.
5. Extender el dashboard con alertas de stock y métricas.

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

Este README se actualizará a medida que el proyecto avance y se implementen nuevas capas y funcionalidades.
