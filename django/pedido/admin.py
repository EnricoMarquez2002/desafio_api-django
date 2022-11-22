from django.contrib import admin

from .models import Pedido, PedidoProduto


class PedidoProdutoInline(admin.TabularInline):
    model = PedidoProduto
    extra = 0
    

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [PedidoProdutoInline]
    list_display = ['numero_pedido', 'status_pedido', 'preco_pedido']



    
    