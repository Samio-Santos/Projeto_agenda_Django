from django.db import models
from contatos.models import Contato
from django.contrib.auth.models import User
from django.contrib.auth import admin as auth_admin

# Create your models here.

class Perfil(models.Model):
    first_name = models.CharField(max_length=35, blank=False, null=False)
    last_name = models.CharField(max_length=35, blank=False, null=False)
    email = models.EmailField(max_length=45, blank=True, null=True)
    # bio = models.TextField(blank=True)
    # imagem = models.ImageField(blank=True, upload_to='fotoPerfil')

    def __str__(self):
        return self.first_name
    



