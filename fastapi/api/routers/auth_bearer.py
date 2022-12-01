from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from .validation import SECRET_KEY, ALGORITHM
from utils.exceptions import exception



class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise exception(403, "Invalid authentication scheme")
            if not self.verify_jwt(credentials.credentials):
                raise exception(403, "invalid token or expired token")
            return self.get_user(credentials.credentials)
        else:
            raise exception(403, "Invalid authorization code")
            
    def verify_jwt(self, jwtoken: str):
        isTokenValid: bool = False
        try:
            payload = jwt.decode(jwtoken, SECRET_KEY, algorithms=[ALGORITHM])
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

    def get_user(self,credenciais: str):
        user = jwt.decode(credenciais, SECRET_KEY, algorithms=[ALGORITHM])
        user = user.get('id')
        return user
