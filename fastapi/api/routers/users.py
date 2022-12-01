from fastapi import APIRouter, Depends
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models
from schemas import UsuarioSchema, UsuarioSchemaUp
from passlib.context import CryptContext
from utils.exceptions import response_message, exception
import datetime
import uuid
from .auth_bearer import JWTBearer




models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return bcrypt_context.hash(password)


def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()


@router.get('', dependencies=[Depends(JWTBearer())])
async def read_users(db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).all()
    if db_user is None:
        raise exception(404, "No users registered yet")
    return db_user

@router.get('/me')
async def read_me(user: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    user = db.query(models.Usuario)\
    .filter(models.Usuario.id_usuario == user)\
    .first()

    print(user)
    if user:
        return user
    raise exception(404, "User not found")


@router.post('')
async def create_user(user: UsuarioSchema, db: Session = Depends(get_db)):
    print(user)

    user_model = models.Usuario()
    user_model.ativo = True
    user_model.data_criacao = datetime.datetime.now()
    user_model.data_modificacao = datetime.datetime.now()
    user_model.id_usuario = uuid.uuid4()
    user_model.nome = user.nome
    user_model.sobrenome = user.sobrenome
    user_model.email = user.email

    hash_password = get_password_hash(user.hashed_password)

    user_model.hashed_password = hash_password

    db.add(user_model)
    db.commit()

    return {
        "status_code" : 201,
        "Detail" : "User created"
    }

@router.patch('/{user_id}', dependencies=[Depends(JWTBearer())])
async def update_user(user_id: str, user: UsuarioSchemaUp, db: Session = Depends(get_db)):
    user_model = db.query(models.Usuario)\
    .filter(models.Usuario.id_usuario == user_id)\
    .first()

    if user_model: 
        user_model.data_modificacao = "2022-11-24" 
        user_model.nome = user.nome
        user_model.sobrenome = user.sobrenome
        user_model.email = user.email

    
        db.commit()

        return response_message(202, "User updated")
    raise exception(404, "User not found")
       
@router.delete('/{user_id}', dependencies=[Depends(JWTBearer())])
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    user_model = db.query(models.Usuario)\
    .filter(models.Usuario.id_usuario == user_id)\
    .first()
    
    if user_model is None:
        raise exception(status_code=404, detail="User not found")
    user_model = db.query(models.Usuario)\
    .filter(models.Usuario.id_usuario == user_id)\
    .delete()

    db.commit()

    return {
        "status": 200,
        "Transaction": "Complete"
    }

