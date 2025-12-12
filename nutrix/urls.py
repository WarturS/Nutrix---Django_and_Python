# nutrix/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # --- URL Principal (Redirecionamento Inteligente) ---
    path('', views.clientes_list, name='clientes_list'),
    
    # --- URLS de Clientes (Nutricionista) ---
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/adicionar/', views.adicionar_cliente, name='adicionar_cliente'),
    path('cliente/<int:pk>/', views.cliente_detail, name='cliente_detail'),
    path('cliente/<int:pk>/editar/', views.editar_cliente, name='editar_cliente'),
    path('cliente/<int:pk>/excluir/', views.excluir_cliente, name='excluir_cliente'),
    
    # --- URLS de Cliente (Usuário Final) ---
    path('cliente/registro/', views.register_client, name='client_register'),
    path('cliente/dashboard/', views.cliente_dashboard, name='cliente_dashboard'),
    
    # --- URLS de Autenticação & Perfis ---
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # CRUCIAL: URL NECESSÁRIA PELO base.html
    path('perfil/', views.perfil_nutricionista, name='perfil_nutricionista'), 
]