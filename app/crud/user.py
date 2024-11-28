from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import User
from app.auth.security import get_current_user
from fastapi import Depends
from app.schemas import UserCreate
from app.models import User
from app.auth.security import hash_password

# Criação do usuário
def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        role=user.role,
        department=user.department,
        hashed_password=hashed_password 
    )

    #Add ao banco
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#  Busca os usuários
def get_users(db: Session, current_user: User = Depends(get_current_user)):
    if current_user.role == "super":
        return db.query(User).all()  # Super pode ver todos os usuários
    return db.query(User).filter(User.department == current_user.department).all()  # Gestor só pode ver usuários do mesmo departamento

# Atualiza um usuário que já existe buscando pelo ID
def update_user(db: Session, user_id: int, updated_user: User, current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if current_user.role == "gestor" and user.department != current_user.department:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    for key, value in updated_user.dict().items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

# Exclui um usuário
def delete_user(db: Session, user_id: int, current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    #Verifica se o funcionário é do departamento do gestor
    if current_user.role == "gestor" and user.department != current_user.department:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
