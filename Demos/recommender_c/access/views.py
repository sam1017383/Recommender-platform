# -*- coding: utf-8 -*-

# **************************************************************
# Programa:     views.py
# Application:  access
# Componente:   vistas 
# Autor:    Carlos A Ulin A
# Empresa:  Infotec
#
# Descripción:
# Este programa contiene las vistas de la aplicación access que
# se encarga de autenticar al usuario mediante el correo y con-
# seña.
# 
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# **************************************************************
# Vista:     Index
#
# Descripción:
# Esta vista se encarga de redirigir al usuario a la página de
# logeo si no tiene sesión de lo contario lo redirige a la app
# products.
# 
# Parámetros:
# @request - Solicita al framework el estatus del usuario
#
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# *************************************************************
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/products/')
    else:
        return render(request, 'access/login.html')


# ****************************************************************
# Vista:     login_view
#
# Descripción:
# Esta vista se encarga de autenticar al usuario con los datos
# proporcionados por el usuario en la página de logeo.
# 
# Parámetros:
# @request - Solicita al framework los campos usuario y contraseña
# proporcionados por el usuario
#
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# ****************************************************************
@csrf_exempt
def login_view(request):
    usuario = request.POST.get('usuario')
    pw = request.POST.get('pw')
    if request.user.is_authenticated():
        return HttpResponseRedirect('/products/')
    user = authenticate(username = usuario, password = pw)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/products/')
        else:
            context = {'errorMessage': 'Usuario inactivo!'}
            return render(request, 'access/login.html', context)
    else:
        context = {'errorMessage': 'Correo Electronico y/o Contrasena incorrecto(s) !'}
        return render(request, 'access/login.html', context)


# ****************************************************************
# Vista:     logut_view
#
# Descripción:
# Esta vista termina la sesión del usuario y lo redirige al login.
# 
# Parámetros:
# @request - Solicita al framework terminar la sesión
#
# Fecha de creación: Marzo-2016
# Versión: 1.0 
# ****************************************************************
@login_required(login_url='/access/login.html')
def logout_view(request):
    logout(request)
    template_name = 'access/login.html'
    return render(request, template_name)
