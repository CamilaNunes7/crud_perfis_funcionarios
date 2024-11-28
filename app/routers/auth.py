from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.models import User
from app.auth.security import create_access_token, verify_password

router = APIRouter()

# Endpoint para realizar login e gerar o token
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    #Verifica se a senha está correta
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    #Gera o token de acesso
    access_token = create_access_token(data={"sub": user.username, "role": user.role, "department": user.department})
    return {"access_token": access_token, "token_type": "bearer"}
