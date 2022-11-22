from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
from pydantic import EmailStr
from utils.timezone import sp
from utils.exceptons import exception


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


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.Usuario)\
    .filter(models.Usuario.nome == username)\
    .first()    

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

    
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

def create_acess_token(username: str, user_id: str, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.now(tz=sp) + expires_delta
    else:
        expire = datetime.now(tz=sp) + timedelta(minutes=5)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  
        user_id: str = payload.get("id")
        if username is None or user_id is None:
            raise exception(404, "User not found")
        return{"username": username, "id": user_id}
    except JWTError:
        raise exception(404, "User not found")

@router.post('/token')
async def login_for_acess_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise exception(404, "Username or password incorrect")
    token_expires = timedelta(minutes=5)
    token = create_acess_token(user.nome, user.id_usuario, expires_delta=token_expires)

    return {"token": token} 

