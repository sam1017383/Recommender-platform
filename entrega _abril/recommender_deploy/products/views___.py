# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404 
from django.conf.urls.static import static
from django.http import Http404, HttpResponse
from django.template import Context, loader
from products.models import *
from django.contrib.auth.decorators import login_required

import recomendaciones_conocimiento
import datetime, random

# Create your views here.
@login_required(login_url='/access/login.html')
def index(request):

     # Esta parte inserta calificaciones de manera aleatoria de los productos especificados
#    productosx = Product.objects.all()
#    usuariosx = Users.objects.all()[:10]    
#    for productox in productosx :
#        for usuariox in usuariosx :
#            try:
#                calificacionE = Calificaciones.objects.get(product=productox, users=usuariox)
#            except Calificaciones.DoesNotExist:
#                comentario = ""
#                valorCalif = random.randint(0, 5)
#                calificacionE = Calificaciones(product=productox, users=usuariox, calificacion_producto=valorCalif, comentario=comentario)
#                calificacionE.save()

    #Aqui debería proponerse un algoritmo que calcule la calificacion promedio de cada producto
    #de manera diaria - Si el promedio es el del dia no se recalculará.
    #En caso de que el promedio sea del dia anterior se recalculará el promedio de manera automática 
    #en cuanto se cargue esta página
    #Evitando de esta manera que el servidor se sobrecargue y el promedio este en tiempo real


    #Se generan las lista que se van a generar en el index
    product_list = Product.objects.all()[1:3]
    usuario_activo = request.user
    usuario = Users.objects.get(pk=usuario_activo.id)
    latest_productos_list_new, metadatos_recomendacion = recomendaciones_conocimiento.recomendacion_por_reglas(usuario)
    latest_productos_list = Product.objects.all()[:20]
    for productoEvaluado in latest_productos_list:
        suma = 0.0
        n = 1
        try:
            calificacionesExistentes = Calificaciones.objects.filter(product=productoEvaluado)
            for calificacionExistente in calificacionesExistentes:
                suma = suma + calificacionExistente.calificacion_producto
                n = n + 1
            calificacion_promedio = suma/(n-1)
            if calificacion_promedio >= 0 and calificacion_promedio <= 0.5:
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
        except Calificaciones.DoesNotExist:
            calificacionesExistentes = None
            calificacion_promedio = 0.0
        try:
            productoExtra = Product_extras.objects.get(Product=productoEvaluado);
            productoExtra.Calificacion_promedio = calificacion_promedio
        except Product_extras.DoesNotExist:
            productoExtra = Product_extras(Product=productoEvaluado, Calificacion_promedio=calificacion_promedio, Precio=0.00, Descuento=0.00);
        productoExtra.save()


    usuario2 = Users.objects.all()[0]
    latest_productos_list2, metadatos_recomendacion2 = recomendaciones_conocimiento.recomendacion_por_reglas(usuario2)

    usuario3 = Users.objects.all()[0]
    latest_productos_list3, metadatos_recomendacion3 = recomendaciones_conocimiento.recomendacion_por_reglas(usuario3)

    usuario4 = Users.objects.all()[0]
    latest_productos_list4, metadatos_recomendacion4 = recomendaciones_conocimiento.recomendacion_por_reglas(usuario4)

    template = loader.get_template('products/index.html')
    context = {
        'latest_productos_list': latest_productos_list[:100],
        'metadatos_usuario': metadatos_recomendacion,
        'latest_productos_list2': latest_productos_list2[:100],
        'metadatos_usuario2': metadatos_recomendacion2,
        'latest_productos_list3': latest_productos_list3[:100],
        'metadatos_usuario3': metadatos_recomendacion3,
        'latest_productos_list4': latest_productos_list4[:100],
        'metadatos_usuario4': metadatos_recomendacion4
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/access/login.html')
def detail(request, product_id):

    #Buscar Lista de Productos recomendados para el usuario
    valorCalificacion = 0
    usuario_activo = request.user
    usuario = Users.objects.get(pk=usuario_activo.id)
    product_list = Product.objects.all()[1:3]
    latest_productos_list, metadatos_recomendacion = recomendaciones_conocimiento.recomendacion_por_reglas(usuario)
    
    #Busca el producto seleccionado
    Producto = get_object_or_404(Product, pk=product_id)

    #Busca objeto de Producto con calificacion para el usuario
    try:
        calificacionExistente = Calificaciones.objects.get(product=Producto, users=usuario)
    except Calificaciones.DoesNotExist:
        comentario = ""
        valorCalificacion = 0
        calificacionExistente = Calificaciones(product=Producto, users=usuario, calificacion_producto=valorCalificacion, comentario=comentario)

    if request.POST.get('comentario') is not None:
        comentario = request.POST.get('comentario')
#        comentario = unicode(comentario, "utf-8")
        calificacionExistente.calificacion_producto=valorCalificacion
        calificacionExistente.comentario=comentario
        calificacionExistente.save()
    else:
        if calificacionExistente.comentario is not None:
            comentario = calificacionExistente.comentario
        else:
            comentario = ""


    if request.POST.get('calificacion') is not None:
        valorCalificacion = request.POST.get('calificacion')
#        calificacionExistente = Calificacionx(productx=Producto, userx=usuario, calificacion_producto=valorCalificacion, comentario=comentario)
        calificacionExistente.calificacion_producto=valorCalificacion
        calificacionExistente.comentario=comentario
        calificacionExistente.save()
    else:
        if calificacionExistente.calificacion_producto is not None:
            valorCalificacion = calificacionExistente.calificacion_producto
        else:
            valorCalificacion = 0

    #Busca comentarios del mismo Producto por otros usuarios
    try:
        comentariosExistentes = Calificaciones.objects.filter(product=Producto).exclude(users=usuario).order_by('-fecha').select_related('users')
    except Calificaciones.DoesNotExist:
        comentariosExistentes = None

    #Construcción del template y envío de Respuesta
    template = loader.get_template('products/detail.html')
    context = {
        'latest_productos_list': latest_productos_list[:150],
        'metadatos_usuario': metadatos_recomendacion,
        'Producto': Producto,
        'id_user': usuario_activo.id,
        'calificacionExistente': calificacionExistente,
        'comentario': comentario,
        'valorCalificacion': valorCalificacion,
        'comentariosExistentes': comentariosExistentes
    }

    return HttpResponse(template.render(context, request))