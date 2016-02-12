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

    class Meta:
    	db_table = 'product'

class Calificaciones(models.Model):
    product = models.ForeignKey(Product)
    users = models.ForeignKey(Users)
    calificacion_producto = models.IntegerField()
    comentario = models.TextField(max_length=1000)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)

    class Meta:
        db_table = 'calificaciones'
