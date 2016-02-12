from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/products/')
    else:
        return render(request, 'access/login.html')

def login_view(request):
    usuario = request.POST.get('usuario')
    pw = request.POST.get('pw')
    user = authenticate(username = usuario, password = pw)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/products/')
        else:
            context = {'errorMessage': 'Usuario inactivo!'}
            return render(request, 'access/login.html', context)
    else:
        context = {'errorMessage': 'Usuario y/o password incorrecto!'}
        return render(request, 'access/login.html', context)

def logout_view(request):
    logout(request)
    template_name = 'access/login.html'
    return render(request, template_name)
