from django.contrib import admin

from .models import Usuario
from pedido.models import Pedido

class PedidoInlines(admin.StackedInline):
    model = Pedido
    extra = 0

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ["nome", "email", "ativo"]
    inlines = [PedidoInlines]

   




