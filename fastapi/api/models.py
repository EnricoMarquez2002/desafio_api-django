from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base  
from sqlalchemy.sql import func
import uuid



class BaseModel(Base):
    __abstract__ = True

    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_modificacao = Column(DateTime(timezone=True), onupdate=func.now())

class Produto(BaseModel):

    __tablename__ = 'produto_produto'

    id_produto = Column(String(32), primary_key=True)
    nome = Column(String(100))
    preco = Column(Float(8,2))
    preco_atual = Column(Float(8,2)) 
    promocao = Column(Boolean, default=False)



class Usuario(BaseModel):
    __tablename__ = 'usuario_usuario'

    id_usuario = Column(String(100), primary_key=True, default=uuid.uuid4)
    nome = Column(String(100))
    email = Column(String(254))
    hashed_password = Column(String(100))
    sobrenome = Column(String(100))
    token_acess = Column(String(300), nullable=True)
    refresh_token = Column(String(300), nullable=True)
    
    pedido_pedido = relationship("Pedido", back_populates="owner")


class Pedido(BaseModel):
    __tablename__ = 'pedido_pedido'

    numero_pedido = Column(String(100), primary_key=True)
    status_pedido = Column(Integer)
    preco_pedido = Column(Float(8,2))
    fk_UUID_usuario_id = Column(String(100), ForeignKey("usuario_usuario.id_usuario", ondelete='CASCADE'), nullable=True)   

    owner = relationship("Usuario", back_populates="pedido_pedido", lazy="joined")
