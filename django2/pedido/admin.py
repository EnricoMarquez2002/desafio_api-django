from django.contrib import admin
from tabbed_admin import TabbedModelAdmin
from .models import Pedido, PedidoProduto


class PedidoProdutoInline(admin.TabularInline):
    model = PedidoProduto
    extra = 1
    

@admin.register(Pedido)
class PedidoAdmin(TabbedModelAdmin):
    inlines = [PedidoProdutoInline]

    tab_overview = (
        (None, {
            'fields': ('numero_pedido', 'status_pedido', 'preco_pedido', 'fk_UUID_usuario')
        }),
        
    )
    tab_produto = (
        PedidoProdutoInline,
    )
    tabs = [
        ('Pedido', tab_overview),
        ('Produtos', tab_produto)
    ]
