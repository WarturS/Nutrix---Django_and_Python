from django.db import models
from django.contrib.auth.models import User  # Importa o modelo User padrão do Django para autenticação


# ============================
# MODELO: CLIENTE
# ============================
class Cliente(models.Model):
    # Relaciona 1 Cliente para 1 User (login do Django)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,   # Se o User for deletado, o Cliente também será
        related_name='cliente'      # Permite acessar: user.cliente
    )

    # Telefone opcional, máximo 20 caracteres
    telefone = models.CharField(max_length=20, blank=True, null=True)

    # Data de nascimento, opcional
    data_nascimento = models.DateField(blank=True, null=True)

    def __str__(self):
        # Representação legível no admin
        return f"Cliente: {self.user.username}"


# ============================
# MODELO: NUTRICIONISTA
# ============================
class Nutricionista(models.Model):
    # Relaciona 1 Nutricionista para 1 User do login
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='nutricionista'  # Acesso via: user.nutricionista
    )

    # Telefone opcional
    telefone = models.CharField(max_length=20, blank=True, null=True)

    # Data opcional
    data_nascimento = models.DateField(blank=True, null=True)

    # CRN do nutricionista — obrigatório e único
    crn = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Nutricionista: {self.user.username}"


# ============================
# MODELO: AGENDAMENTO
# ============================
class Agendamento(models.Model):
    # Indica qual nutricionista disponibilizou esse horário
    nutricionista = models.ForeignKey(
        Nutricionista,
        on_delete=models.CASCADE,       # Apaga agendamentos se o nutricionista for apagado
        related_name='agendamentos'     # Acesso: nutricionista.agendamentos.all()
    )

    # Data do agendamento
    data = models.DateField()

    # Hora do agendamento
    hora = models.TimeField()

    # Define se o horário está disponível ou não
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.data} {self.hora} - {self.nutricionista.user.username}"


# ============================
# MODELO: CONSULTA
# ============================
class Consulta(models.Model):
    # Cliente que marcou essa consulta
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='consultas'    # Acesso: cliente.consultas.all()
    )

    # Agendamento escolhido — um horário só pode ter 1 consulta
    agendamento = models.OneToOneField(
        Agendamento,
        on_delete=models.CASCADE
    )

    # Lista de status possíveis
    STATUS_CHOICES = [
        ("Pendente", "Pendente"),
        ("Realizada", "Realizada"),
        ("Cancelada", "Cancelada"),
    ]

    # Status da consulta
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pendente"
    )

    def __str__(self):
        return f"Consulta de {self.cliente.user.username} em {self.agendamento.data} {self.agendamento.hora}"


# ============================
# MODELO: PLANO ALIMENTAR
# ============================
class PlanoAlimentar(models.Model):
    # Um plano alimentar está sempre ligado a uma consulta específica
    consulta = models.OneToOneField(
        Consulta,
        on_delete=models.CASCADE
    )

    # Conteúdo do plano alimentar escrito pelo nutricionista
    descricao = models.TextField()

    # Data automatica de criação
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Plano Alimentar da consulta {self.consulta.id}"
