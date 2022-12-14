from django.db import models
from app_config.models import BaseModel
import uuid


class Usuario(BaseModel):
    id_usuario = models.CharField(
       default= uuid.uuid4,
       max_length=36,
       unique=True,
       primary_key=True,
       editable=False,
    )
    nome = models.CharField("Nome", max_length=100, unique=False)
    sobrenome = models.CharField("Sobrenome", max_length=100, unique=False, default=None)
    email = models.EmailField("E-mail", unique=True)
    hashed_password = models.CharField(
        "Senha", 
        max_length=100,
        default=None,
    )
    token_acess = models.CharField("Token_acess", max_length=300, unique=True, null=True)
    refresh_token = models.CharField("refresh token", max_length=300, unique=True, null=True)


    def __str__(self) -> str:
        return self.nome

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"