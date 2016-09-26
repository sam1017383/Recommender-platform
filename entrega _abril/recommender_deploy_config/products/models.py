# -*- coding: utf-8 -*-

# **************************************************************
# Programa:     models.py
# Application:  products
# Componente:   Modelos
# Autor:    Carlos A Ulin A
# Empresa:  Infotec
#
# Descripción:
# En este programa se declaran los modelos necesarios para el 
# funcionamiento correcto de la app products.
# 
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************

from __future__ import unicode_literals
from datetime import datetime, date
from django.utils import timezone
from django.db import models

# Create your models here.

# **************************************************************
# Modelo:     Users
#
# Descripción:
# Este modelo representa la estructura de la tabla users. 
# 
# Metodos:
# N/A
#
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************
class Users(models.Model):
    Nombre = models.CharField(max_length=255)
    CP = models.CharField(max_length=255)
    Genero = models.CharField(max_length=255)
    Apellido_p = models.CharField(max_length=255)
    Apellido_m = models.CharField(max_length=255)
    Ciudad = models.CharField(max_length=255)
    Hijos = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)
    Estado_civil = models.CharField(max_length=255)
    Contacto = models.CharField(max_length=255)
    Nacimiento = models.CharField(max_length=255)

    class Meta:
    	db_table = 'users'

# **************************************************************
# Modelo:     Product
#
# Descripción:
# Este modelo representa la estructura de la tabla product. 
# 
# Metodos:
# _get_calificacion(): Obtiene el valor de la calificacion del 
#                      producto de la tabla Calificaciones
# _get_precio()      : Obtiene el valor de la calificacion del 
#                      producto de la tabla Calificaciones
# _get_descuento()   : Obtiene el valor de la calificacion del 
#                      producto de la tabla Calificaciones
# _get_imagen()      : Obtiene el valor de la calificacion del 
#                      producto de la tabla Calificaciones
# 
# Propiedades:
# ref_calificacion  : Valor de la calificación del oroducto
# ref_precio        : Valor del precio del producto
# ref_descuento     : Valor del descuento aplicables al producto
# ref_imagen        : Nombre de la imagen del producto
#
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************
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

    def natural_key(self):
        return '%s %s' % (self.Categoria, self.Latitud)

    def _get_calificacion(self):
        "Regresa la calificacion promedio del producto en la tabla product_extras"
        extras_producto = Product_extras.objects.get(Product=self.id)
        return str(extras_producto.Calificacion_promedio)

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
        if extras_producto.Imagen_fuente is None:
            extras_producto.Imagen_fuente = 'image/farmacia01.jpg'
        return str(extras_producto.Imagen_fuente)


    ref_calificacion = property(_get_calificacion)
    ref_precio = property(_get_precio)
    ref_descuento = property(_get_descuento)
    ref_imagen = property(_get_imagen)


    class Meta:
        db_table = 'product'

# **************************************************************
# Modelo:     Product_extras
#
# Descripción:
# Este modelo representa la estructura de la tabla product_extras. 
# 
# Metodos:
# _calculaPromedio():  Calcula el valor promedio de las califica- 
#                      ciones de los usuarios a un producto
# 
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************
class Product_extras(models.Model):
    Product = models.OneToOneField(Product)
    Imagen_fuente = models.CharField(max_length=255)
    Calificacion_promedio = models.FloatField()
    Precio = models.DecimalField(max_digits=10, decimal_places=2)
    Descuento = models.DecimalField(max_digits=3, decimal_places=2)
    Fecha_alta = models.DateField(auto_now_add=True)
    Fecha_calculo = models.DateField(default=datetime.now, blank=True)
    
    def calculaPromedio(self, Producto=Product):        
        try:
            productoExtra = Product_extras.objects.get(Product=Producto)
        except Product_extras.DoesNotExist:
            productoExtra = Product_extras(Product=Producto, Calificacion_promedio=calificacion_promedio, Precio=0.00, Descuento=0.00)
        fechaActual = date.today()
        if productoExtra.Fecha_calculo is None or productoExtra.Fecha_calculo < fechaActual:
            calificacion_promedio = 0.0
            productoExtra.Fecha_calculo = fechaActual
            suma = 0.0
            n = 1
            try:
                calificacionesExistentes = Calificaciones.objects.filter(product=Producto)
                for calificacionExistente in calificacionesExistentes:
                    suma = suma + calificacionExistente.calificacion_producto
                    n = n + 1
                if n > 1:
                    calificacion_promedio = suma/(n-1)
                else:
                    calificacion_promedio = suma/n
                if calificacion_promedio == 0:
                    calificacion_promedio = 0.00
                if calificacion_promedio > 0 and calificacion_promedio <= 0.5:
                    calificacion_promedio = 0.50
                if calificacion_promedio > 0.5 and calificacion_promedio <= 1.0:
                    calificacion_promedio = 1.00   
                if calificacion_promedio > 1.0 and calificacion_promedio <= 1.5:
                    calificacion_promedio = 1.50
                if calificacion_promedio > 1.5 and calificacion_promedio <= 2.0:
                    calificacion_promedio = 2.00
                if calificacion_promedio > 2.0 and calificacion_promedio <= 2.5:
                    calificacion_promedio = 2.50
                if calificacion_promedio > 2.5 and calificacion_promedio <= 3.0:
                    calificacion_promedio = 3.00
                if calificacion_promedio > 3.0 and calificacion_promedio <= 3.5:
                    calificacion_promedio = 3.50
                if calificacion_promedio > 3.5 and calificacion_promedio <= 4.0:
                    calificacion_promedio = 4.00
                if calificacion_promedio > 4.0 and calificacion_promedio <= 4.5:
                    calificacion_promedio = 4.50
                if calificacion_promedio > 4.5 and calificacion_promedio <= 5.0:
                    calificacion_promedio = 5.00
                productoExtra.Calificacion_promedio = calificacion_promedio
                productoExtra.save()
            except Calificaciones.DoesNotExist:
                calificacionesExistentes = None
                calificacion_promedio = 0.0        
        return productoExtra

    def natural_key(self):
        return '%s %s' % (self.Product, self.Calificacion_promedio)

    class Meta:
        db_table = 'product_extras'

# **************************************************************
# Modelo:     Calificaciones
#
# Descripción:
# Este modelo representa la estructura de la tabla calificaciones. 
# 
# Metodos:
# N/A
# 
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************
class Calificaciones(models.Model):
    product = models.ForeignKey(Product)
    users = models.ForeignKey(Users)
    calificacion_producto = models.IntegerField()
    comentario = models.TextField(max_length=1000)
    fecha = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"), blank=True)
    hora = models.TimeField(default=datetime.datetime.now().strftime("%H:%M:%S"), blank=True)

    class Meta:
        db_table = 'calificaciones'




class Listas_recomendadores_config(models.Model):
    id = models.AutoField(primary_key=True)
    titulo_interfaz = models.CharField(max_length=255)
    algoritmo_recomendador = models.CharField(max_length=100)
    longitud_max = models.IntegerField()
    param = models.FloatField()
    secuencia = models.IntegerField(default=0)



    class Meta:
        db_table = 'listas_recomendadores_config'
