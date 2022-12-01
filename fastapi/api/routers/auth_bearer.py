from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

SECRET_KEY = '$2b$12$W6R/MU2YOPss.RGn6oCOb.2A.I1Fh.pwQ6Yz3a0rN7.qimUsBhKhe'
ALGORITHM = 'HS256'

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="invalid token or expired token")
            return self.get_user(credentials.credentials)
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code")
            
    def verify_jwt(self, jwtoken: str):
        isTokenValid: bool = False
        try:
            payload = jwt.decode(jwtoken, SECRET_KEY, algorithms=[ALGORITHM])
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

    def get_user(self,credenciais:str):
        user = jwt.decode(credenciais, SECRET_KEY, algorithms=[ALGORITHM])
        user = user.get('id')
        return user
