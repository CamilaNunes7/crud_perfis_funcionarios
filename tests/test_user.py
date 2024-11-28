import pytest
from fastapi.testclient import TestClient
from app.database import Base, engine, SessionLocal
from app.models import User
from app.auth.security import hash_password
from app.main import app

# Configuração do cliente para chamadas à API
client = TestClient(app)

# Configuração do banco de dados para os testes
@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Fixture para criar usuários adicionais para os testes
@pytest.fixture(scope="module")
def create_test_users(db_session):
    test_users = [
        User(
            first_name="John",
            last_name="Doe",
            username="john_doe",
            email="john@example.com",
            role="comercial",
            department="RH",
            hashed_password=hash_password("password123"),
        ),
        User(
            first_name="Jane",
            last_name="Doe",
            username="jane_doe",
            email="jane@example.com",
            role="gestor",
            department="RH",
            hashed_password=hash_password("password123"),
        ),
    ]
    db_session.add_all(test_users)
    db_session.commit()
    return test_users


# Teste para verificar a visualização de usuários pelo gestor no próprio departamento
def test_gestor_view_own_department(create_test_users):
    gestor_token = "Bearer VALID_GESTOR_TOKEN"
    response = client.get(
        "/users/",
        headers={"Authorization": gestor_token}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3  # O gestor deve ver 3 usuários: admin, jhon_doe e jane_doe


# Teste para verificar a visualização de usuários pelo super
def test_super_view_all_users(create_test_users):
    super_token = "Bearer VALID_SUPER_TOKEN"  
    response = client.get(
        "/users/",
        headers={"Authorization": super_token}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3  # O super deve ver todos os usuários no sistema


# Teste para verificar que o gestor só vê usuários de sua área
def test_gestor_cannot_view_other_department(create_test_users):
    gestor_token_ti = "Bearer VALID_GESTOR_TOKENTI"
    response = client.get(
        "/users/",
        headers={"Authorization": gestor_token_ti}
    )
    assert response.status_code == 200
    data = response.json()
    # Verifica se apenas usuários do departamento RH estão visíveis
    for user in data:
        assert user["department"] == "RH"

    # Verifica que o gestor não vê usuários de outros departamentos
    hr_user_exists = any(user["department"] == "HR" for user in data)
    assert not hr_user_exists, "O gestor do departamento TI não deve ver usuários do departamento RH"

# Teste para deletar um usuário
def test_delete_user(db_session):
    user_to_delete = db_session.query(User).filter(User.username == "jane_doe").first()
    assert user_to_delete is not None, "O usuário test_user deve existir para ser deletado."
    db_session.delete(user_to_delete)
    db_session.commit()

    user_check = db_session.query(User).filter(User.username == "test_user").first()
    assert user_check is None, "O usuário test_user deve ter sido deletado."