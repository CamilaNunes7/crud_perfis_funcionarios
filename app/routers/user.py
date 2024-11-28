from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.schemas import UserCreate, UserOut, UserUpdate
from app.models import Base,User
from app.auth.dependencies import get_current_user
from typing import List

router = APIRouter()

# Inicializar o banco de dados
Base.metadata.create_all(bind=engine)


@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Verifica se o usuário atual tem permissão para criar usuários
    if current_user["role"] not in ["super", "gestor"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Cria um novo usuário
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        role=user.role,
        department=user.department
    )
    # Define a senha (aplica o hash)
    db_user.set_password(user.password)
    
    # Add ao banco
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()  # Recupera todos os usuários do banco de dados
    return users

@router.get("/{name}", response_model=List[UserOut])
def search_users_by_name(name: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Se o usuário for "super", ele pode buscar usuários em qualquer departamento
    if current_user["role"] == "super":
        users = db.query(User).filter(
            (User.first_name.ilike(f"%{name}%")) | (User.last_name.ilike(f"%{name}%"))
        ).all()
    else:
        # Um gestor só pode buscar usuários do próprio departamento
        users = db.query(User).filter(
            (User.department == current_user["department"]) &
            ((User.first_name.ilike(f"%{name}%")) | (User.last_name.ilike(f"%{name}%")))
        ).all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found with the given name")
    
    return users


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, updated_user: UserUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Busca o usuário no banco
    user = db.query(User).filter(User.id == user_id).first()

    # Verifica se ele existe e suas permissões
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user["role"] == "gestor" and user.department != current_user["department"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    # Atualiza os campos
    for key, value in updated_user.dict(exclude_unset=True).items():
        setattr(user, key, value)

    # Add alteração no banco
    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Busca o usuário no banco
    user = db.query(User).filter(User.id == user_id).first()

    # Verifica se ele existe e suas permissões
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user["role"] == "gestor" and user.department != current_user["department"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    # Remove o usuário 
    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
