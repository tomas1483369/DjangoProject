from django.contrib import admin

from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'precio', 'cantidad', 'stock_minimo', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre', 'codigo')
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')
