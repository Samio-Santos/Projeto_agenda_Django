from django.forms import ModelForm
from contatos.models import Contato
from django.contrib.auth.models import User

class Contatoform(ModelForm):
    class Meta:
        model = Contato
        fields = '__all__'


class Userform(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'bio', 'imagem')
    
    