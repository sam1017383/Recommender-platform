from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    Genero = models.CharField(max_length=255)
    Nacimiento = models.CharField(max_length=255)
    Apellido_p = models.CharField(max_length=255)
    Apellido_m = models.CharField(max_length=255)
    Ciudad = models.CharField(max_length=255)
    Hijos = models.CharField(max_length=255)
    Estado_civil = models.CharField(max_length=255)
    Nombre = models.CharField(max_length=255)
    Contacto = models.CharField(max_length=255)
    CP = models.CharField(max_length=255)
    id_usuario = models.IntegerField()
    def __str__(self):
        return self.Nombre + " " + self.Apellido_p


class Product(models.Model):
    Categoria = models.CharField(max_length=255)
    Latitud = models.CharField(max_length=255)
    Contacto = models.CharField(max_length=255)
    Colonia = models.CharField(max_length=255)
    Direccion = models.CharField(max_length=255)
    Alias = models.CharField(max_length=255)
    Longitud = models.CharField(max_length=255)
    Nombre = models.CharField(max_length=255)
    Descripcion = models.CharField(max_length=255)
    CP = models.CharField(max_length=255)
    Estado = models.CharField(max_length=255)
    Municipio = models.CharField(max_length=255)
    id_producto = models.IntegerField()
    def __str__(self):
        return self.Categoria + " " + self.Nombre
