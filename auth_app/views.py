from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required

# Create your views here.
def cadastro(request):
  if request.method == "GET":
    return render(request, 'cadastro.html')
  else:
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = User.objects.filter(username=username).first()
    if user:
      return HttpResponse('Nome de usuário já existe.')
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    return HttpResponse('Usuário ' + username + ' cadastrado com sucesso.')

def login(request):
  if request.method == "GET":
    return render(request, 'login.html')
  else:
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
      django_login(request, user)
      return HttpResponse('Autenticado com sucesso! Bem vindo ' + username + '.')
    else:
      return HttpResponse('Usuário ou senha inválidos.')

"""
def home(request):
  if request.user.is_authenticated:
    return render(request, 'home.html')
  return render(request, 'login.html')
"""

@login_required(login_url='/auth/login/')
def home(request):
  return render(request, 'home.html')