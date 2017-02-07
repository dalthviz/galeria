import json

from django.contrib.auth import authenticate, login, logout
from django.core import serializers

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Imagen, ImageForm, UserForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# Create your views here.
@csrf_exempt
def index(request):
    if request.user.is_authenticated():
        lista_imagenes = Imagen.objects.filter(user=request.user)
    else:
        lista_imagenes = Imagen.objects.all()
    context = {'lista_imagenes': lista_imagenes}
    return HttpResponse(serializers.serialize('json', lista_imagenes))

@csrf_exempt
def add_image(request):
    if request.method == 'POST':
        post = request.POST
        new_image = Imagen(url=post['url'],
                           title=post['title'],
                           description=post.get('description'),
                           type=post.get('type'),
                           imageFile=request.FILES['imageFile'],
                           user=request.user)
        new_image.save()
    return HttpResponse(serializers.serialize('json', [new_image]))

@csrf_exempt
def add_user_view(request):
    if request.method == 'POST':
        jsonUser = json.loads(request.body)
        username = jsonUser['username']
        first_name = jsonUser['first_name']
        last_name = jsonUser['last_name']
        password = jsonUser['password']
        email = jsonUser['email']

        user_model = User.objects.create_user(username=username, password=password)
        user_model.first_name = first_name
        user_model.last_name = last_name
        user_model.email = email
        user_model.save()
    return  HttpResponse(serializers.serialize('json', [user_model]))

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        jsonUser = json.loads(request.body)
        username = jsonUser['username']
        password = jsonUser['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            mensaje = 'ok'
        else:
            mensaje = 'Nombre de usuario o clave no valido'
    return JsonResponse({'mensaje':mensaje})

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'mensaje':'ok'})

@csrf_exempt
def islogged_view(request):
    if request.user.is_authenticated:
        mensaje = 'ok'
    else:
        mensaje = 'no'
    return JsonResponse({'mensaje': mensaje})

def ver_imagenes(request):
    return render(request, "polls/index.html");

def agregar_imagen(request):
    return render(request, "polls/image_form.html");

def agregar_usuario(request):
    return render(request, "polls/registro.html");

def ingresar(request):
    return render(request, "polls/login.html");


