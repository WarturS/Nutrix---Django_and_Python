from django.contrib import admin
from .models import Nutricionista, Cliente, Agendamento, Consulta, PlanoAlimentar


""""
@admin.register(Nutricionista)
class NutricionistaAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "registro")


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "email")


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ("nutricionista", "data", "hora", "disponivel")
    list_filter = ("data", "nutricionista", "disponivel")


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ("cliente", "agendamento", "status")
    list_filter = ("status",)


@admin.register(PlanoAlimentar)
class PlanoAlimentarAdmin(admin.ModelAdmin):
    list_display = ("consulta", "criado_em")
"""