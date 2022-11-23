from django.contrib import admin
from tabbed_admin import TabbedModelAdmin
from .models import Usuario
from pedido.models import Pedido

class PedidoInlines(admin.StackedInline):
    model = Pedido
    extra = 0

@admin.register(Usuario)
class UsuarioAdmin(TabbedModelAdmin):
    inlines = [PedidoInlines]
    
    tab_overview = (
        (None, {
            'fields': ('nome', 'email', 'ativo')
        }),
        
    )
    tab_pedido = (
        PedidoInlines,
    )
    tabs = [
        ('Usuário', tab_overview),
        ('Pedidos', tab_pedido)
    ]
   




