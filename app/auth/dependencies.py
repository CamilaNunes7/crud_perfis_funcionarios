from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from app.auth.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Função para validar o token JWT e obter os dados do usuário
# Se válido retorna os dados, se inválido  ou expirado retorna um erro
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload 
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

