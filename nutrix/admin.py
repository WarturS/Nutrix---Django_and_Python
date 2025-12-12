# nutrix/admin.py
from django.contrib import admin
from .models import Nutricionista, Cliente

# Configuração para o modelo Nutricionista
class NutricionistaAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'registro')
    search_fields = ('user__username', 'registro')
    
    # Método customizado para exibir o username do usuário relacionado
    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Usuário (Login)'

# Configuração para o modelo Cliente
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nutricionista_nome', 'email', 'data_agendamento', 'imc')
    search_fields = ('nome', 'email', 'nutricionista__user__username')
    list_filter = ('nutricionista',)
    
    # Método customizado para exibir o nome do Nutricionista
    def nutricionista_nome(self, obj):
        return obj.nutricionista.user.get_full_name() or obj.nutricionista.user.username
    nutricionista_nome.short_description = 'Nutricionista'

# Registra os modelos no painel administrativo
admin.site.register(Nutricionista, NutricionistaAdmin)
admin.site.register(Cliente, ClienteAdmin)