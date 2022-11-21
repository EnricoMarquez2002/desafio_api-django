from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models
from schemas import UsuarioSchema, UsuarioSchemaUp
from passlib.context import CryptContext

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


@router.get('')
async def read_users(db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).all()
    if db_user is None:
        raise HTTPException(status_code=404, detail="No users registered yet")
    return db_user


@router.get('/{user_id}')
async def read_user_name(user_id: str, db: Session = Depends(get_db)):
    user_name_model = db.query(models.Usuario)\
    .filter(models.Usuario.id_usuario == user_id)\
    .first()
    if user_name_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_name_model


@router.post('')
async def create_user(user: UsuarioSchema, db: Session = Depends(get_db)):
    user_model = models.Usuario()
    user_model.ativo = user.ativo
    user_model.data_criacao = user.data_criacao
    user_model.data_modificacao = user.data_modificacao
    user_model.id_usuario = user.id_usuario
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

@router.patch('')
async def update_user(user_id: str, user: UsuarioSchemaUp, db: Session = Depends(get_db)):
    user_model = db.query(models.Usuario)\
    .filter(models.Usuario.id_usuario == user_id)\
    .first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_model = models.Usuario
    user_model.ativo = user.ativo
    user_model.data_criacao = user.data_criacao
    user_model.data_modificacao = user.data_modificacao
    user_model.id_usuario = user.id_usuario
    user_model.nome = user.nome
    user_model.sobrenome = user.sobrenome
    user_model.email = user.email
    user_model.hashed_password = user.hashed_password
   
    db.add(models.Usuario)
    db.commit()

    return {
        "status": 200,
        "Detail": "User updated"
    }

@router.delete('/{user_id}')
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    user_model = db.query(models.Usuario)\
    .filter(models.Usuario.id_usuario == user_id)\
    .first()
    
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_model = db.query(models.Usuario)\
    .filter(models.Usuario.id_usuario == user_id)\
    .delete()

    db.commit()

    return {
        "status": 200,
        "Transaction": "Complete"
    }

