from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .form import Contatoform, Userform


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    
    usuario = request.POST.get('user')
    senha = request.POST.get('password')

    # faz uma requisição nos campos de usuário e senha
    user = auth.authenticate(request, username=usuario, password=senha)
    
    # Verifica se o usuário e senha são válidos
    if not user:
        messages.error(request, 'Usuário ou senha invalidos.')
        return render(request, 'accounts/login.html')
    
    else:
        auth.login(request, user)
        return redirect ('dashboard')
    
def logout(request):
    auth.logout(request)
    return redirect('login')


def cadastro(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('snome')
    email = request.POST.get('email')
    usuario = request.POST.get('user')
    senha = request.POST.get('password')
    rsenha = request.POST.get('rsenha')
    foto = request.POST.get('file')


    # Verifica se nem um campo está vazio
    if not nome or not sobrenome or not email or not usuario or not senha or not rsenha:
        messages.error(request, 'Nenhum campo pode ficar vázio!')
        return render(request, 'accounts/cadastro.html')
    
    # Valida o email
    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido!')
        return render(request, 'accounts/cadastro.html')
    
    # Valida a Senha
    if len(senha) < 6:
        messages.error(request, 'Senha muito curta! Senha presica ter no minimo 6 caracteres ou mais.')
        return render(request, 'accounts/cadastro.html')

    # Verifica se as senhas são iguais
    if senha != rsenha:
        messages.error(request, 'Senhas não são iguais! Tente novamente.')
        return render(request, 'accounts/cadastro.html')

    # Valida o usuario
    if len(usuario) < 6:
        messages.error(request, 'Usuario presica ter 6 caracteres ou mais.')
        return render(request, 'accounts/cadastro.html')
    
    # Verifica se o usuario já existe
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuario já existe!')
        return render(request, 'accounts/cadastro.html')
    
    # Verifica se o email já existe
    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já existe!')
        return render(request, 'accounts/cadastro.html')

    # Se tudo ocorre bem o usuario será criado
    messages.success(request, 'Usuario registrado com sucesso! Agora faça login.')
    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)

    user.save()
    return redirect('login')


# Um decorador que verifica se o usuario está logado
# Se não estiver logado o usuario será redirecionado para a tela de login
@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = Contatoform()
        return render(request, 'accounts/dashboard.html', {'form': form})
    
    form = Contatoform(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao enviar formulário.')
        form = Contatoform(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})
    
    descricao = request.POST.get('descricao')

    if len(descricao) < 5:
        messages.error(request, 'Descrição precisa ter mais de 5 caracteres.')
        form = Contatoform(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'Contato {request.POST.get("nome")} {request.POST.get("sobrenome")} salvo com sucesso.')
    return redirect('dashboard')


def perfil_update(request, id):
    data = {}
    user = User.objects.get(id=id)
    form  = Userform(request.POST or None, request.FILES or None, instance=user)

    data['user'] = user
    data['form'] = form

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados atualizados com sucesso')
            return redirect('dashboard')
    
    else:
        return render(request, 'accounts/perfil.html', data)
