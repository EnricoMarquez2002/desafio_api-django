from django.contrib import admin

from .models import Produto
from pedido.models import PedidoProduto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco_atual','promocao', 'data_criacao']

