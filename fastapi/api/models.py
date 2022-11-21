from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, BigInteger
from sqlalchemy.orm import relationship
from database import Base  



class Produto(Base):
    __tablename__ = 'produto_produto'

    ativo = Column(Boolean, default=True) 
    data_criacao = Column(DateTime)
    data_modificacao = Column(DateTime)
    id_produto = Column(String(32), primary_key=True)
    nome = Column(String(100))
    preco = Column(Float(8,2))
    preco_atual = Column(Float(8,2)) 
    promocao = Column(Boolean, default=False)

    #produto_produto = relationship("PedidoProduto", back_populates="owner")


class Usuario(Base):
    __tablename__ = 'usuario_usuario'

    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime)
    data_modificacao = Column(DateTime)
    id_usuario = Column(String(36), primary_key=True)
    nome = Column(String(100))
    email = Column(String(254))
    hashed_password = Column(String(100))
    sobrenome = Column(String(100))

    pedido_pedido = relationship("Pedido", back_populates="owner", cascade="all, delete")


class Pedido(Base):
    __tablename__ = 'pedido_pedido'

    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime)
    data_modificacao = Column(DateTime)
    numero_pedido = Column(String(100), primary_key=True)
    status_pedido = Column(Integer)
    preco_pedido = Column(Float(8,2))
    fk_UUID_usuario_id = Column(String(100), ForeignKey("usuario_usuario.id_usuario"))   

    owner = relationship("Usuario", back_populates="pedido_pedido", lazy="joined")


    #pedido_pedido = relationship("PedidoProduto", back_populates="pedido_owner")


"""
class PedidoProduto(Base):
    __tablename__ = 'pedido_pedidoproduto'

id = Column(BigInteger, primary_key=True, autoincrement=True)
ativo = Column(Boolean, default=True)
data_criacao = Column(DateTime)
data_modificacao = Column(DateTime)
preco_produto = Column(Float(8,2))
quantidade = Column(Integer)
fk_id_produto_id = Column(String(100), ForeignKey("produto_produto.id_produto"))
fk_numero_pedido_id = Column(String(100), ForeignKey("pedido_pedido.numero_pedido"))

owner = relationship("Produto", back_populates="produto_produto")
pedido_owner = relationship("Pedido", back_populates="pedido_pedido")
"""