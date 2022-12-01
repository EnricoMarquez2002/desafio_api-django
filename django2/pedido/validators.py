from django.core.exceptions import ValidationError


status_pedido = [1, 2, 3, 4]


def valida_status(value):
    if value == status_pedido[1]:
        raise ValidationError("O pedido foi cancelado")
    if value == status_pedido[3]:
        raise ValidationError("O pedido foi concluído")
    else:
        return "Pedido atualizado"

def convert_to_cents(value):    
    price = value
    if price < 0:
        raise ValidationError("Price must be positive")
    else:
        price *=100
    return price    



