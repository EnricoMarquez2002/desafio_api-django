from django.db import models
from app_config.models import BaseModel
from usuario.models import Usuario
from produto.models import Produto
import uuid
from .validators import valida_status


STATUS_CHOICES = [
    (1, "Iniciado"),
    (2, "Cancelado"),
    (3,"Faturado"),
    (4, "Concluído")
]

class Pedido(BaseModel):
    numero_pedido = models.CharField(
        "Número do pedido",
        max_length=100,
        default=uuid.uuid4, 
        primary_key=True,
        editable=False

    )
    status_pedido = models.IntegerField("Status do pedido", choices=STATUS_CHOICES, validators=[valida_status])
    preco_pedido = models.DecimalField("Preço do pedido", max_digits=8, decimal_places=2)
    fk_UUID_usuario = models.ForeignKey(Usuario, verbose_name="Usuário", null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:   
        return f"Pedido número: {self.numero_pedido}"

    class Meta:
        verbose_name="Pedido"
        verbose_name_plural="Pedidos"


class PedidoProduto(BaseModel):
    fk_id_produto = models.ForeignKey(Produto, verbose_name="Id do produto", on_delete=models.CASCADE)
    fk_numero_pedido = models.ForeignKey(Pedido, verbose_name="Numero do pedido", on_delete=models.CASCADE)
    preco_produto = models.DecimalField("Preço do produto", max_digits=9, decimal_places=2)
    quantidade = models.IntegerField("Quantidade")

    class Meta:
        verbose_name="Produto"
        verbose_name_plural="Carrinho de compras"
