from django.db import models
from app_config.models import BaseModel
import uuid 

class Produto(BaseModel):
    id_produto = models.CharField(
        default=uuid.uuid4,
        max_length=36,
        unique=True,
        primary_key=True,
        editable=False
    )
    nome = models.CharField("Nome", max_length=100)
    preco=models.DecimalField("Preço", max_digits=8, decimal_places=2)
    preco_atual=models.DecimalField("Preço atual", max_digits=8, decimal_places=2)
    promocao = models.BooleanField("Está na promoção?")

    def __str__(self) -> str:
        return self.nome

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        