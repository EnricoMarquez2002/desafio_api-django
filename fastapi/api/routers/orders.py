from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models
from schemas import PedidoSchema, PedidoSchemaUp
from utils.exceptions import response_message, exception
from .auth_bearer import JWTBearer
import datetime
import uuid



models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    dependencies=[Depends(JWTBearer())]
)

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()


@router.get('')
async def read_orders(db: Session = Depends(get_db)):
    db_order = db.query(models.Pedido).first()
    if db_order is None:
        raise exception(404, "No orders found")
    return db_order


@router.get('/{user_id}')
async def read_orders_by_user_id(user_id: str, db: Session = Depends(get_db)):
    db_order_user_id = db.query(models.Pedido)\
    .filter(models.Pedido.fk_UUID_usuario_id == user_id)\
    .all()

    if db_order_user_id is None:
        raise HTTPException(status_code=404, detail="User ID not found")
    return db_order_user_id


@router.post('')
async def create_order(order: PedidoSchema, db: Session = Depends(get_db)):
    order_model = models.Pedido()
    order_model.ativo = True
    order_model.data_criacao = datetime.datetime.now()
    order_model.data_modificacao = datetime.datetime.now() 
    order_model.numero_pedido =uuid.uuid4()
    order_model.status_pedido = 1
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

    if order_model.status_pedido == 2:
        raise exception(400, "Cannot update order, it has been cancel")
    if order_model.status_pedido == 4:
        raise exception(400, "Cannot update order, it has been concluded")

    if order_model:
        order_model.data_modificacao = order.data_modificacao
        order_model.status_pedido = order.status_pedido
        order_model.preco_pedido = order.preco_pedido

        db.commit()

        return response_message(200, "Order updated")
    raise exception(404, "Order not found")        
    