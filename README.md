# Guia de autentificação com Django

## Índice

1. [Iniciando projeto](#start)
2. [Criando Super usuário](#createsuperuser)
3. [Usando a classe User](#django_user)
4. [Fazendo Login](#login)

- [Referências](#refs)

<div id="start" />

## Iniciando Projeto

  Nesse exemplo vamos usar a própria classe User que o Django fornece por padrão.

  Antes de começar, precisar saber a base do Django, já ter criado, o nosso 'auth_app' e as views 'cadastro' e 'login'.

<div id="createsuperuser" />

## Criando Super usuário

  Para gerenciar os usuários cadastrados, precisamos de um administrador do sistema. Para isso usamos o seguinte comando no terminal:

  ```
  $ python manage.py createsuperuser
  ```

  Com o administrador criado vamos na URL: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) e logar como administrador.

<div id="django_user" />

## Usando a classe User

  Para utilizar o model.User que o Django oferece por padrão adicionamos o seguinte código nas nossas views:

  ```python
  from django.contrib.auth.models import User

  # Cria um usuário
  user = User.objects.create_user(username=username, email=email, password=password)

  # Salva o usuário no banco de dados 
  user.save()

  # Requisição ao Banco de Dados do usuário
  user = User.objects.filter(username=username).first()
  ```

  No exemplo o nosso arquivo de 'view.py' fica assim:

  ```python
  from django.http.response import HttpResponse
  from django.shortcuts import render
  from django.contrib.auth.models import User

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
  ```

<div id="login" />

## Fazendo Login

  Para fazer login no projeto vamos criar uma view 'home' e 'login', que será o caminho '/' do projeto e que somente usuários logados terão acesso.

  'auth_dango/urls.py'
  ```python
  from django.contrib import admin
  from django.urls import path, include
  from auth_app.views import home

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('auth/', include('auth_app.urls')),
      path('', home, name='home'),
  ]
  ```

  'auth_app/templates/home.html'
  ```html
  {% extends 'layout.html' %}
  {% block title %}
    <title>Home</title>
  {% endblock %}
  {% block content %}
    <h1>Home</h1>
  {% endblock %}
  ```

  'auth_app/urls.py'
  ```python
  from django.urls import path
  from . import views

  urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
  ]
  ```

  'auth_app/templates/login.html'
  ```html
  {% extends 'layout.html' %}
  {% block title %}
    <title>Login</title>
  {% endblock %}
  {% block content %}
    <form action="{% url 'login' %}" method="post">
      {% csrf_token %}
      <input type="text" name="username" id="username" placeholder="username">
      <br>
      <input type="password" name="password" id="password" placeholder="password">
      <br>
      <input type="submit" value="login">
    </form>
  {% endblock %}
  ```

  Agora no nosso app/views vamos adicionar as seguintes linhas.

  'auth_app/views.py'
  ```python
  from django.contrib.auth import authenticate
  from django.contrib.auth import login as django_login
  from django.contrib.auth.decorators import login_required

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

  @login_required(login_url='/auth/login/')
  def home(request):
    return render(request, 'home.html')
  ```

  Observe que o método 'authenticate' no 'login' verifica se as informações daquele usuário que está tentando logar, são as mesmas do usuário no sistema.

  Quando esse requisito é verdadeiro, a método django_login cria a sessão do usuário

  E na view 'home' o '@login_required' faz a verificação se a sessão já existe, caso não exista redireciona para 'auth/login', e quando existe um usuário logado com sucesso permite o acesso ao conteúdo de home.html.

  Como se fosse assim:

  ```python
  def home(request):
    # O @login_required tire a condição da view, separando o código
    if request.user.is_authenticated:
      return render(request, 'home.html')
    return render(request, 'login.html')
  ```


<div id="refs">

## Referências



[Autentificação com Django](https://youtu.be/gdhiA6wObw0?si=bgo_cmSCrETXAHGQ)
