# nutrix/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Cliente, Nutricionista
from .forms import ClienteForm, ClientUserCreationForm 

# --- Funções de Teste de Usuário (Controle de Acesso) ---

def is_nutricionista(user):
    """Verifica se o usuário logado possui um perfil de Nutricionista."""
    if user.is_authenticated:
        return hasattr(user, 'nutricionista')
    return False

def is_client(user):
    """Verifica se o usuário logado possui um perfil de Cliente."""
    if user.is_authenticated:
        return hasattr(user, 'cliente') and not hasattr(user, 'nutricionista')
    return False

# ----------------------------------------------------------------------
# VIEWS DE AUTENTICAÇÃO E REDIRECIONAMENTO
# ----------------------------------------------------------------------

def clientes_list(request):
    """
    URL RAIZ e LISTA DE CLIENTES: Redireciona usuários logados para o painel correto.
    Se for Nutricionista, mostra a lista de clientes.
    """
    if not request.user.is_authenticated:
        return redirect('login')
        
    if is_nutricionista(request.user):
        nutricionista = get_object_or_404(Nutricionista, user=request.user)
        clientes = Cliente.objects.filter(nutricionista=nutricionista).order_by('nome')
        return render(request, 'nutrix/clientes_list.html', {'clientes': clientes})
    elif is_client(request.user):
        return redirect('cliente_dashboard')
    else:
        return HttpResponseForbidden("Sua conta não tem um painel de acesso configurado.")


def login_view(request):
    """Lida com o login e o redirecionamento inteligente."""
    
    if request.user.is_authenticated:
        if is_nutricionista(request.user):
            return redirect('clientes_list')
        elif is_client(request.user):
            return redirect('cliente_dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Login realizado. Bem-vindo(a), {user.username}!")
            
            if is_nutricionista(user):
                return redirect('clientes_list')
            elif is_client(user):
                return redirect('cliente_dashboard')
            else:
                return redirect('clientes_list')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            
    return render(request, 'nutrix/login.html')

def logout_view(request):
    """Encerra a sessão do usuário."""
    if request.user.is_authenticated:
        messages.info(request, "Sessão encerrada. Até logo!")
        logout(request)
    return redirect('login')

# ----------------------------------------------------------------------
# VIEWS DE CRUD DE CLIENTES (Nutricionista) - RESTAURADAS
# ----------------------------------------------------------------------

@login_required
@user_passes_test(is_nutricionista, login_url='/login/')
def adicionar_cliente(request):
    """Processa o formulário e salva um novo cliente vinculado ao Nutricionista logado."""
    nutricionista = get_object_or_404(Nutricionista, user=request.user)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES) 
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.nutricionista = nutricionista 
            cliente.save()
            
            messages.success(request, f"Cliente {cliente.nome} adicionado com sucesso!")
            
            return redirect('clientes_list') 
    else:
        form = ClienteForm() 
        
    return render(request, 'nutrix/adicionar_cliente.html', {'form': form})


@login_required
@user_passes_test(is_nutricionista, login_url='/login/')
def cliente_detail(request, pk):
    """Exibe os detalhes de um cliente específico."""
    # Garante que só clientes DESSE nutricionista podem ser vistos
    nutricionista = get_object_or_404(Nutricionista, user=request.user)
    cliente = get_object_or_404(Cliente, pk=pk, nutricionista=nutricionista)
    
    return render(request, 'nutrix/cliente_detail.html', {'cliente': cliente})


@login_required
@user_passes_test(is_nutricionista, login_url='/login/')
def editar_cliente(request, pk):
    """Lida com a edição de um cliente existente."""
    nutricionista = get_object_or_404(Nutricionista, user=request.user)
    cliente = get_object_or_404(Cliente, pk=pk, nutricionista=nutricionista)

    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente) 
        if form.is_valid():
            form.save() 
            
            messages.success(request, f"Cliente {cliente.nome} atualizado com sucesso!")
            
            return redirect('cliente_detail', pk=cliente.pk) 
    else:
        form = ClienteForm(instance=cliente)
        
    context = {
        'form': form,
        'cliente': cliente
    }
    return render(request, 'nutrix/editar_cliente.html', context)


@login_required
@user_passes_test(is_nutricionista, login_url='/login/')
def excluir_cliente(request, pk):
    """Lida com a exclusão de um cliente existente."""
    nutricionista = get_object_or_404(Nutricionista, user=request.user)
    cliente = get_object_or_404(Cliente, pk=pk, nutricionista=nutricionista)
    
    if request.method == 'POST':
        cliente_nome = cliente.nome 
        cliente.delete()
        
        messages.success(request, f"Cliente {cliente_nome} excluído permanentemente.")
        
        return redirect('clientes_list') 
    
    return render(request, 'nutrix/excluir_cliente_confirmar.html', {'cliente': cliente})


# ----------------------------------------------------------------------
# VIEWS DE CLIENTE (Usuário)
# ----------------------------------------------------------------------

def register_client(request):
    """Lida com o registro de um novo usuário (Cliente)."""
    if request.method == 'POST':
        form = ClientUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # ATENÇÃO: Vincula ao Nutricionista 'nutri2' para testes.
            try:
                nutricionista = Nutricionista.objects.get(user__username='nutri2')
            except Nutricionista.DoesNotExist:
                messages.error(request, "Erro: O Nutricionista 'nutri2' não existe no sistema.")
                user.delete()
                return redirect('client_register')

            Cliente.objects.create(
                user=user,
                nutricionista=nutricionista,
                nome=user.first_name or user.username,
            )

            messages.success(request, "Cadastro realizado! Faça login para acessar sua área.")
            return redirect('login') 
        else:
            messages.error(request, "Erro no cadastro. Verifique os campos.")
    else:
        form = ClientUserCreationForm()
    
    return render(request, 'nutrix/client_register.html', {'form': form})

@login_required
@user_passes_test(is_client, login_url='/login/')
def cliente_dashboard(request):
    """Painel do Cliente: Exibe seus dados e agendamentos feitos pelo nutri2."""
    cliente = get_object_or_404(Cliente, user=request.user)
    
    context = {
        'cliente': cliente,
    }
    return render(request, 'nutrix/cliente_dashboard.html', context)


# ----------------------------------------------------------------------
# VIEW DE PERFIL (Nutricionista)
# ----------------------------------------------------------------------

@login_required
def perfil_nutricionista(request):
    """Exibe o perfil e informações do Nutricionista logado."""
    
    if is_nutricionista(request.user):
        nutricionista = get_object_or_404(Nutricionista, user=request.user)
        return render(request, 'nutrix/perfil.html', {'nutricionista': nutricionista})
    else:
        # Clientes não têm acesso a esta tela de perfil de Nutricionista
        return redirect('cliente_dashboard')