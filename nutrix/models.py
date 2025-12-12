# nutrix/models.py
from django.db import models
from django.contrib.auth.models import User

# -----------------------------------------------------------
# MODELO NUTRICIONISTA (MANTER O VÍNCULO)
# -----------------------------------------------------------

class Nutricionista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Adicione ou mantenha seus campos específicos do Nutricionista
    registro = models.CharField(max_length=50, unique=True, default='CRN-0000') 
    
    def __str__(self):
        return f"Nutri: {self.user.username}"
    
    @property
    def nome_completo(self):
        return self.user.get_full_name() or self.user.username

# -----------------------------------------------------------
# MODELO CLIENTE (VÍNCULO AO USUÁRIO DE LOGIN E AGENDAMENTOS)
# -----------------------------------------------------------

class Cliente(models.Model):
    # CRUCIAL: Vínculo ao usuário de login
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Vincula o cliente ao seu Nutricionista
    nutricionista = models.ForeignKey(Nutricionista, on_delete=models.CASCADE, related_name='clientes')
    
    # Dados do cliente
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    altura = models.FloatField(null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)
    
    # Campos para Agendamento do Nutricionista
    data_agendamento = models.DateTimeField(null=True, blank=True)
    google_meet_link = models.URLField(blank=True, null=True)
    condicao_agendamento = models.CharField(max_length=100, blank=True, null=True)    

    @property
    def imc(self):
        if self.altura and self.peso and self.altura > 0:
            return round(self.peso / (self.altura ** 2), 2)
        return None

    def __str__(self):
        return self.nome