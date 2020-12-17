from django.urls import path
from .views import (
    login, logout, cadastro, dashboard,
    perfil_update
)

urlpatterns = [
    path('', login, name='index_login'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('cadastro/', cadastro, name='cadastro'),
    path('dashboard/', dashboard, name='dashboard'),
    path('perfil/<int:id>/', perfil_update, name='perfil_update'),
 
]
