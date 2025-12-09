from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/novo/', views.cliente_form, name='cliente_form'),
    path('clientes/<int:id>/editar/', views.cliente_form, name='cliente_edit'),
    path('clientes/<int:id>/deletar/', views.cliente_delete, name='cliente_delete'),
]
