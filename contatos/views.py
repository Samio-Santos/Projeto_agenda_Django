from django.shortcuts import render, get_object_or_404, redirect
from .models import Contato, Categoria
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages

# Create your views here.


def index(request):
    data = {}

    # pega todos os dado no banco de dados e ordena pelo id em ordem decrecente
    contatos = Contato.objects.order_by('-id')

    # cria paginações na minha agenda
    paginator = Paginator(contatos, 5)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    data['pessoa'] = contatos
    return render(request, 'contatos/index.html', data)


# Para pegar informações individuais acessando pelo ID
# Não interavel
# colocar diretamente no template, ex: {{contato.nome do dado que você deseja mostrar}}]
# get_object_or_404, caso uma pagina não ser encontrada o servidor mostra pagina não encontrada
def detalhe_contato(request, id):
    data = {}
    contato = get_object_or_404(Contato, id=id)

    # Verifica se pode mostrar o dado
    if not contato.mostrar:
        raise Http404()

    data['contato'] = contato
    return render(request, 'contatos/detalhe.html', data)


def busca(request):
    data = {}
    termo = request.GET.get('termo')
    campos =  Concat('nome', Value(' '), 'sobrenome')

    # Verifica se o termo existe ou está vázio, caso esteja vázio, emite uma mensagem de erro
    if termo is None or not termo:
        messages.add_message(
            request, 
            messages.ERROR, 
            'O campo de busca não pode ficar vázio'
        )
        return redirect('index')

    contatos = Contato.objects.annotate(
        nome_completo=campos
     ).filter(
        # '__icontains' verifica se tem parte do texto que o usuario digitou na busca.

        # 'Q' permite fazer um buscar mais avançada e exata, ou é um ou é outro
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
     )
     
    # cria paginações na minha agenda
    paginator = Paginator(contatos, 5)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    data['pessoa'] = contatos
    return render(request, 'contatos/busca.html', data)