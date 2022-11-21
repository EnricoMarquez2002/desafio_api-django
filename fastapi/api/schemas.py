from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List
from datetime import datetime
import uuid
import re

class UsuarioSchema(BaseModel):
    ativo: bool
    data_criacao: datetime = Field(default_factory=datetime.utcnow)
    data_modificacao: datetime = Field(default_factory=datetime.utcnow)
    id_usuario: uuid.UUID = Field(default_factory=uuid.uuid4(), primary_key=True, index=True, unique=True)
    nome: str
    sobrenome: str
    email: EmailStr
    hashed_password: str

    @validator('hashed_password')
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError("Password must be longer tha 8 digits")
        if not re.search('[A-Z]', value):
            raise ValueError("Password must have at least one upper digit")
        if not re.search("[0-9]", value):
            raise ValueError("Password must have ate lesat one number")
        if not re.search(r"[ `!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?~]", value):
            raise ValueError("Password must have at least one special digit")
        return value


class UsuarioSchemaUp(BaseModel):
    ativo: Optional[bool]
    data_criacao: Optional[datetime] = Field(default_factory=datetime.utcnow)
    data_modificacao: Optional[datetime] = Field(default_factory=datetime.utcnow)
    id_usuario: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4(), primary_key=True, index=True, unique=True)
    nome: Optional[str]
    email: Optional[EmailStr]
    hashed_password: Optional[str]
    sobrenome: Optional[str]

class ProdutoSchema(BaseModel):
    ativo: bool
    data_criacao: datetime = Field(default_factory=datetime.utcnow)
    data_modificacao: datetime = Field(default_factory=datetime.utcnow)
    id_produto: uuid.UUID = Field(default_factory=uuid.uuid4(), primary_key=True, index=True, unique=True)
    nome: str
    preco: float
    preco_atual: float
    promocao: bool = False

class ProdutoSchemaUp(ProdutoSchema):
    ativo: Optional[bool]
    data_criacao: Optional[datetime] = Field(default_factory=datetime.utcnow)
    data_modificacao: Optional[datetime] = Field(default_factory=datetime.utcnow)
    id_produto: Optional [str]
    nome: Optional[str]
    preco: Optional[float]
    preco_atual: Optional[float]
    promocao: Optional[bool] = False


class PedidoSchema(BaseModel):
    ativo: Optional[bool]
    data_criacao: datetime = Field(default_factory=datetime.utcnow)
    data_modificacao: datetime = Field(default_factory=datetime.utcnow)
    numero_pedido: str
    status_pedido: int
    preco_pedido: float
    fk_UUID_usuario_id: str
    
    class Config:
        orm_mode=True

