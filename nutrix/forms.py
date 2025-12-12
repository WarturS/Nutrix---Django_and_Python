# nutrix/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente

# -----------------------------------------------------------
# NOVO: FORMULÁRIO DE CRIAÇÃO DE USUÁRIO CLIENTE
# -----------------------------------------------------------

class ClientUserCreationForm(UserCreationForm):
    """
    Formulário para criar um novo usuário que será associado a um perfil de Cliente.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Torna o email obrigatório no registro
        self.fields['email'].required = True 

# -----------------------------------------------------------
# FORMULÁRIO DE CLIENTE (Usado pelo Nutricionista)
# -----------------------------------------------------------

class ClienteForm(forms.ModelForm):
    """
    Formulário para o Nutricionista adicionar ou editar os dados de um cliente.
    """
    class Meta:
        model = Cliente
        fields = [
            'nome', 
            'email',
            'altura', 
            'peso', 
            'data_agendamento', 
            'google_meet_link', 
            'condicao_agendamento'
        ]
        
        widgets = {
            'data_agendamento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }