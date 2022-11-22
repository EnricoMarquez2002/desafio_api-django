from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models
from schemas import PedidoSchema, PedidoSchemaUp
from .validation import get_current_user
from utils.exceptons import response_message, exception

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()


@router.get('')
async def read_orders(db: Session = Depends(get_db)):
    db_order = db.query(models.Pedido).all()
    if db_order is None:
        raise exception(404, "Order not found")
    return db_order


@router.get('/{user_id}')
async def read_orders_by_user_id(user_id: str, db: Session = Depends(get_db)):
    db_order_user_id = db.query(models.Pedido)\
    .filter(models.Pedido.fk_UUID_usuario_id == user_id)\
    .all()

    if db_order_user_id is None:
        raise HTTPException(status_code=404, detail="User ID not found")
    return db_order_user_id

@router.get('/{order_id}')
async def read_order_by_order_id(order_id: str, db: Session = Depends(get_db)):
    db_order_id = db.query(models.Pedido)\
    .filter(models.Pedido.numero_pedido == order_id)\
    .first()

    if db_order_id is None:
        raise exception(404, "Order id not found")
    return db_order_id


@router.post('')
async def create_order(order: PedidoSchema, db: Session = Depends(get_db)):
    order_model = models.Pedido()
    order_model.ativo = order.ativo
    order_model.data_criacao = order.data_criacao
    order_model.data_modificacao = order.data_modificacao
    order_model.numero_pedido = order.numero_pedido
    order_model.status_pedido = order.status_pedido
    order_model.preco_pedido = order.preco_pedido
    order_model.fk_UUID_usuario_id = order.fk_UUID_usuario_id

    if order_model is None:
        raise exception(404, "User not found")
        
    db.add(order_model)
    db.commit()

    return response_message(201, "Order Created")

@router.delete('/{order_id}')
async def delete_order_by_id(order_id: str, db: Session = Depends(get_db)):
    db_model = db.query(models.Pedido)\
    .filter(models.Pedido.numero_pedido == order_id)\
    .first()
     
    if db_model is None:
        raise HTTPException(status_code=404, detail="order_id not found")
    db_model = db.query(models.Pedido)\
    .filter(models.Pedido.numero_pedido == order_id)\
    .delete()
     
    db.commit()

    return response_message(200, "Order Deleted")
       

@router.patch('/{order_id}')
async def update_order(order_id: str, order: PedidoSchemaUp, db: Session = Depends(get_db)):
    order_model = db.query(models.Pedido)\
    .filter(models.Pedido.numero_pedido == order_id)\
    .first() 

    if order_model:
        order_model.data_modificacao = order.data_modificacao
        order_model.status_pedido = order.status_pedido
        order_model.preco_pedido = order.preco_pedido

        db.commit()

        return response_message(200, "Order updated")
    raise exception(404, "Order not found")        
    