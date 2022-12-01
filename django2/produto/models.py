from django.db import models
from app_config.models import BaseModel
import uuid 
from pedido.validators import convert_to_cents

class Produto(BaseModel):
    id_produto = models.CharField(
        default=uuid.uuid4,
        max_length=100,
        unique=True,
        primary_key=True,
        editable=False
    )
    nome = models.CharField("Nome", max_length=100)
    preco=models.DecimalField("Preço", max_digits=8, decimal_places=2, validators=[convert_to_cents])
    preco_atual=models.DecimalField("Preço atual", max_digits=8, decimal_places=2, validators=[convert_to_cents])
    promocao = models.BooleanField("Está na promoção?")

    def __str__(self) -> str:
        return self.nome

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
    