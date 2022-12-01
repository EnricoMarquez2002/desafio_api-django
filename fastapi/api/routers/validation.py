from fastapi import APIRouter, Depends, HTTPException, Request, Body
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models
from passlib.context import CryptContext
from pydantic import EmailStr
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
from utils.timezone import sp
from utils.exceptions import exception
from schemas import RefreshTokenSchema

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    tags=["Validation"]
)

SECRET_KEY = '$2b$12$W6R/MU2YOPss.RGn6oCOb.2A.I1Fh.pwQ6Yz3a0rN7.qimUsBhKhe'
ALGORITHM = 'HS256'


def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

#criar função get user

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)

def update_acess_token(user_id: str, token: str):
    try:
        db=SessionLocal()
        db.query(models.Usuario)\
        .filter(models.Usuario.id_usuario == user_id)\
        .update({"token_acess": token})

        db.commit()
    finally:
        db.close()


def update_refresh_token(user_id: str, token: str):
    try:
        db=SessionLocal()
        db.query(models.Usuario)\
        .filter(models.Usuario.id_usuario == user_id)\
        .update({"refresh_token": token})

        db.commit()
    finally:
        db.close()



def create_acess_token(email: EmailStr, user_id: str, hashed_pass: str, expires_delta: Optional[timedelta] = None):
    encode = {"sub": email, "id": user_id,"hashed":hashed_pass}
    if expires_delta:
        expire = datetime.now(tz=sp) + expires_delta
    else:
        expire = datetime.now(tz=sp) + timedelta(minutes=5)
    encode.update({"exp": expire})
    jwtac = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    update_acess_token(user_id, jwtac)
    return {
        "Token": jwtac,
        "expires": expire
    }


def create_refresh_token(email: EmailStr, user_id: str, expires_delta: Optional[timedelta] = None):
    encode = {"sub": email, "id": user_id}
    if expires_delta:
        expire = datetime.now(tz=sp) + expires_delta
    else:
        expire = datetime.now(tz=sp) + timedelta(minutes=20)
    encode.update({"exp": expire})
    jwtre = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    update_refresh_token(user_id, jwtre)
    return {
        "Refresh Token": jwtre,
        "expires": expire,
    }



@router.post('/auth/login')
async def user_login(email: EmailStr, password: str, db: Session = Depends(get_db)):
    user = db.query(models.Usuario)\
    .filter(models.Usuario.email == email)\
    .first()

    if user is None:
        return exception(404, "User not found")
    if verify_password(password, user.hashed_password):
        return create_acess_token(email,user.id_usuario,user.hashed_password), create_refresh_token(email, user.id_usuario)
    raise exception(404, "Incorrect password") 


@router.post('auth/refresh')
async def refresh_token(token:RefreshTokenSchema, db: Session = Depends(get_db)):
    user = db.query(models.Usuario)\
    .filter(models.Usuario.refresh_token == token)\
    .first()

    user = models.Usuario
    user.refresh_token = token.refresh_token

    print(user)
    if user:
        return create_refresh_token(email, user.id_usuario)
    raise exception(404, "not found")

        