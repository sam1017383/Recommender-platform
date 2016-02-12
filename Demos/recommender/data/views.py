from django.shortcuts import render, get_object_or_404 
from django.http import Http404, HttpResponse
from django.template import Context, loader
from django.contrib.auth.models import User
from data.models import *

import datetime

# Create your views here.
def index(request):
    users_list = Users.objects.all()
    estatus = "Sin iniciar"

    for usuario in users_list:

        # Process the data in Usuarios Table
        username = "micorreonuevo@localhost.com"
        password = "Password_"+str(usuario.id)
    
        if usuario.Contacto is not None:
            email=usuario.Contacto
        else:
            email = "micorreonuevo@localhost.com"
    
        if usuario.Contacto is not None:
            username = usuario.Contacto
        else:
            username = "micorreonuevo@localhost.com"

        first_name = usuario.Nombre
        last_name = usuario.Apellido_p
    
        #actualUser = User.objects.get(pk=2) 
        #actualUser.delete()    
        try:
            actualUser = User.objects.get(username=username)
        except User.DoesNotExist:    
            actualUser = User.objects.create_user(username, email, password, id=usuario.id)
            actualUser.first_name = first_name
            actualUser.last_name = last_name

    estatus = "Terminado"

    template = loader.get_template('data/index.html')
    context = {
        'estatus': estatus
    }
    return HttpResponse(template.render(context, request))