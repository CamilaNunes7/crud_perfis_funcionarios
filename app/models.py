from sqlalchemy import Column, Integer, String
from app.database import Base

# Define modelo de dados da tabela de usuários
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)  # 'super' ou 'gestor'
    department = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Função que recebe a senha em texto e converte para um hash
    def set_password(self, password: str):
        from app.auth.security import hash_password
        self.hashed_password = hash_password(password)
