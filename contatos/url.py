from django.urls import path
from .views import (
    index, detalhe_contato, busca
)

urlpatterns = [
    path('index/', index, name='index'),
    path('busca/', busca, name='busca'),
    path('<int:id>', detalhe_contato, name='contato_detalhe'),
]