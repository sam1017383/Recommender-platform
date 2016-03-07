from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Users(models.Model):
    Nombre = models.CharField(max_length=255)
    CP = models.CharField(max_length=255)
    Genero = models.CharField(max_length=255)
    Apellido_p = models.CharField(max_length=255)
    Apellido_m = models.CharField(max_length=255)
    Ciudad = models.CharField(max_length=255)
    Hijos = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=255)
    Estado_civil = models.CharField(max_length=255)
    Contacto = models.CharField(max_length=255)
    Nacimiento = models.CharField(max_length=255)

    class Meta:
    	db_table = 'users'

class Product(models.Model):
    Categoria = models.CharField(max_length=255)
    Latitud = models.CharField(max_length=255)
    Contacto = models.CharField(max_length=255)
    Colonia = models.CharField(max_length=255)
    Direccion = models.CharField(max_length=255)
    Alias = models.CharField(max_length=255)
    Calificable = models.BooleanField(default=1)
    Longitud = models.CharField(max_length=255)
    Nombre = models.CharField(max_length=255)
    Descripcion = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)
    CP = models.CharField(max_length=255)
    Estado = models.CharField(max_length=255)
    Municipio = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s %s' % (self.categoria, self.latitud)

    def _get_calificacion(self):
        "Regresa la calificacion promedio del producto en la tabla product_extras"
        extras_producto = Product_extras.objects.get(Product=self.id)
        return str(extras_producto.Calificacion)

    def _get_precio(self):
        "Regresa el precio del producto en la tabla product_extras"
        extras_producto = Product_extras.objects.get(Product=self.id)
        return str(extras_producto.Precio)

    def _get_descuento(self):
        "Regresa el decuento del producto en la tabla product_extras"
        extras_producto = Product_extras.objects.get(Product=self.id)
        return str(extras_producto.Descuento)

    def _get_imagen(self):
        "Regresa la ruta de imagen del producto en la tabla product_extras"
        extras_producto = Product_extras.objects.get(Product=self.id)
        return str(extras_producto.Imagen_fuente)


    ref_calificacion = property(_get_calificacion)
    ref_precio = property(_get_precio)
    ref_descuento = property(_get_descuento)
    ref_imagen = property(_get_imagen)


    class Meta:
    	db_table = 'product'

class Product_extras(models.Model):
    Product = models.ForeignKey(Product)
    Imagen_fuente = models.CharField(max_length=255)
    Calificacion = models.FloatField()
    Precio = models.FloatField()
    Descuento = models.FloatField()
    id = models.AutoField(primary_key=True)
    Fecha = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return '%s %s' % (self.product, self.Calificacion)

    class Meta:
        db_table = 'product_extras'


class Calificaciones(models.Model):
    product = models.ForeignKey(Product)
    users = models.ForeignKey(Users)
    calificacion_producto = models.IntegerField()
    comentario = models.TextField(max_length=1000)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)

    class Meta:
        db_table = 'calificaciones'
