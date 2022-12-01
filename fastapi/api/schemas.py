from pydantic import BaseModel, validator, EmailStr
from typing import Optional
from datetime import datetime
import re




class UsuarioSchema(BaseModel):
    nome: str
    sobrenome: str
    email: EmailStr
    hashed_password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "nome": "nome",
                "sobrenome": "sobrenome",
                "email": "user@exemplo.com",
                "hashed_password": "Senha@123"
            }
        }

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
    nome: Optional[str]
    email: Optional[EmailStr]
    sobrenome: Optional[str]
    hashed_password: Optional[str]

    class Config:
        schema_extra = {
            "example":{
                "nome": "nome",
                "sobrenome": "sobrenome",
                "email": "user@exemplo.com",
                "hashed_password": "Exemplo!123"
            }   
        }



class ProdutoSchema(BaseModel):
    nome: str
    preco: float
    preco_atual: float
    promocao: bool = False

class ProdutoSchemaUp(BaseModel):
    nome: Optional[str]
    preco_atual: Optional[float]
    promocao: Optional[bool] 


class PedidoSchema(BaseModel):
    status_pedido: int = 1
    preco_pedido: float
    fk_UUID_usuario_id: str
    
    class Config:
        orm_mode=True


class PedidoSchemaUp(BaseModel):
    status_pedido: Optional[int]
    preco_pedido: Optional[float]
    
    class Config:
        orm_mode = True 


class RefreshTokenSchema(BaseModel):
    refresh_token: str