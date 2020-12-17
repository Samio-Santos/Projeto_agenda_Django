from django.db import models
from django.utils import timezone

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=35, blank=False, null=False)

    def __str__(self):
        return self.nome


class Contato(models.Model):
    nome = models.CharField(max_length=35, blank=False, null=False)
    sobrenome = models.CharField(max_length=35, blank=False, null=False)
    telefone = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(max_length=45, blank=True, null=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    imagem = models.ImageField(blank=True, upload_to='imagens/')
    mostrar = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nome}'
