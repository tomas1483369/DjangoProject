from django.db import models


class ProductoQuerySet(models.QuerySet):
    def activos(self):
        return self.filter(estado=True)

    def bajo_stock(self):
        return self.filter(cantidad__lte=models.F('stock_minimo'), cantidad__gt=0)

    def agotados(self):
        return self.filter(cantidad=0)


class ProductoManager(models.Manager):
    def get_queryset(self):
        return ProductoQuerySet(self.model, using=self._db)

    def activos(self):
        return self.get_queryset().activos()

    def bajo_stock(self):
        return self.get_queryset().bajo_stock()

    def agotados(self):
        return self.get_queryset().agotados()
