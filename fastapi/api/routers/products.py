from fastapi import Depends, HTTPException, APIRouter    
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models
from schemas import ProdutoSchema, ProdutoSchemaUp
from utils.exceptions import response_message, exception
import datetime
import uuid
from .auth_bearer import JWTBearer



models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[Depends(JWTBearer())]
)


def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()


@router.get('')
async def read_products(db: Session = Depends(get_db)):
    db_product = db.query(models.Produto)\
    .all()

    if db_product:
        return db_product   
    raise exception(404, "No products registered yet")


@router.get('/{product_id}')
async def read_product_by_id(product_id: str, db: Session = Depends(get_db)):
    db_product_id = db.query(models.Produto)\
    .filter(models.Produto.id_produto == product_id)\
    .first()
    if db_product_id is None:
        raise exception(404, "Product_id not found")
    return db_product_id

@router.post('', status_code=201)
async def create_products(product: ProdutoSchema, db: Session = Depends(get_db)):
    db_product = models.Produto()
    db_product.ativo = True
    db_product.data_criacao = datetime.datetime.now()
    db_product.data_modificacao = datetime.datetime.now()
    db_product.id_produto = uuid.uuid4()
    db_product.nome = product.nome
    db_product.preco = product.preco    

    db_product.preco *= 100

    db_product.preco_atual = product.preco_atual

    db_product.preco_atual *= 100 

    db_product.promocao = product.promocao

    db.add(db_product)
    db.commit()

    return response_message(201, "Product Created")
     


@router.patch('/{product_id}')
async def update_product(product_id: str, product: ProdutoSchemaUp, db: Session = Depends(get_db)):
    db_product_id = db.query(models.Produto)\
    .filter(models.Produto.id_produto == product_id)\
    .first()

    if db_product_id:
        db_product_id.data_modificacao = datetime.datetime.now()
        db_product_id.nome = product.nome
        db_product_id.preco_atual = product.preco_atual

        db_product_id.preco_atual *= 100 

        db_product_id.promocao = False

        db.commit()

        return response_message(202, "Product Updated")
    raise exception(404, "Product id not found")


@router.delete('/{product_id}')
async def delete_product(product_id: str, db: Session = Depends(get_db)):
    db_product_id = db.query(models.Produto)\
    .filter(models.Produto.id_produto == product_id)\
    .first()
    if db_product_id is None:
        raise HTTPException(status_code=404, detail="Product id not found")
    db.query(models.Produto)\
    .filter(models.Produto.id_produto == product_id)\
    .delete()
    
    db.commit()

    return response_message(200, "Product Deleted")
