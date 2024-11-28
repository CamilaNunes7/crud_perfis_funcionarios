import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app.models import User
from sqlalchemy.orm import sessionmaker
from app.auth.security import hash_password

# Configurações do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)  # Limpa o banco antes de cada teste
Base.metadata.create_all(bind=engine)  # Cria as tabelas para o teste

# Substitui a dependência do banco de dados
@pytest.fixture(scope="module")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

client = TestClient(app)

# Cria um usuário de teste chamado 'admin'
@pytest.fixture(scope="module", autouse=True)
def create_test_user(db):
    test_user = User(
        first_name="Admin",
        last_name="User",
        username="admin",
        email="admin@example.com",
        role="super",
        department="RH",
        hashed_password=hash_password("password123"),
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)


# Teste para verificar se o usuário criado consegue logar
def test_login_success():
    response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

# Teste para verificar se o usuário consegue logar com senha errada
def test_login_invalid_credentials():
    response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "wrongpassword"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid credentials"