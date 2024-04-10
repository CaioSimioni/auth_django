# Guia de autentificação com Django

## Índice

1. [Iniciando projeto](#start)

- [Referências](#refs)

<div id="start" />

## Iniciando Projeto

  Nesse exemplo vamos usar a própria classe User que o Django fornece por padrão.

  Antes de começar, precisar saber a base do Django, já ter criado, o nosso 'auth_app' e as views 'cadastro' e 'login'.

  ## Criando Super usuário

  Para gerenciar os usuários cadastrados, precisamos de um administrador do sistema. Para isso usamos o seguinte comando no terminal:

  ```
  $ python manage.py createsuperuser
  ```

  Com o administrador criado vamos na URL: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) e logar como administrador.

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

<div id="refs">

## Referências



[Autentificação com Django](https://youtu.be/gdhiA6wObw0?si=bgo_cmSCrETXAHGQ)
