# CRUD Perfis de Funcionários

Um projeto desenvolvido em Python para realizar operações de **CRUD (Create, Read, Update, Delete)** com um banco de dados PostgreSQL utilizando SQLAlchemy como ORM.

Este projeto tem como objetivo gerenciar informações de funcionários, incluindo nome, idade, cargo e outras informações pertinentes.

---

## 🛠 Tecnologias Utilizadas

- **FastAPI**: Framework para construir a API de maneira rápida e eficiente.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **Pydantic**: Biblioteca para validação de dados e criação de modelos de entrada e saída.
- **JWT (JSON Web Tokens)**: Para autenticação segura.
- **bcrypt**: Para criptografar senhas dos usuários.
- **SQLite**: Banco de dados utilizado durante o desenvolvimento.

---

## ⚙️ Funcionalidades

- **Cadastro de Usuário**: O administrador pode criar novos usuários fornecendo as informações necessárias, incluindo nome, email, senha e cargo.
- **Login**: O usuário pode fazer login utilizando um nome de usuário e senha válidos, recebendo um token JWT como resposta.
- **Visualização de Usuários**:
  - O **super** pode visualizar todos os usuários do sistema.
  - O **gestor** pode visualizar apenas os usuários do seu próprio departamento.
- **Atualização de Usuário**: O usuário pode ser atualizado, mas um **gestor** só pode atualizar os usuários do seu próprio departamento.
- **Exclusão de Usuário**: O **gestor** só pode excluir usuários do seu próprio departamento.

---
## Endpoints da API

### Autenticação

- **POST /auth/login**:
  - Realiza o login e retorna um token de acesso.
  - **Body**:
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
  - **Resposta**:
    ```json
    {
      "access_token": "string",
      "token_type": "bearer"
    }
    ```

### Usuários

- **POST /users/**: Cria um novo usuário.
  - **Body**:
    ```json
    {
      "first_name": "string",
      "last_name": "string",
      "username": "string",
      "email": "string",
      "role": "string",
      "department": "string",
      "password": "string"
    }
    ```

- **GET /users/**: Lista todos os usuários (somente para **super**).
  - **Resposta**:
    ```json
    [
      {
        "id": 1,
        "first_name": "string",
        "last_name": "string",
        "username": "string",
        "email": "string",
        "role": "string",
        "department": "string"
      }
    ]
    ```

- **GET /users/{name}**: Busca um usuário pelo nome.
  - **Resposta**:
    ```json
    {
      "id": 1,
      "first_name": "string",
      "last_name": "string",
      "username": "string",
      "email": "string",
      "role": "string",
      "department": "string"
    }
    ```

- **PUT /users/{id}**: Atualiza um usuário.
  - **Body**:
    ```json
    {
      "first_name": "string",
      "last_name": "string",
      "username": "string",
      "email": "string",
      "role": "string",
      "department": "string",
      "password": "string" (opcional)
    }
    ```

- **DELETE /users/{id}**: Deleta um usuário.
  - **Resposta**:
    ```json
    {
      "message": "User deleted successfully"
    }
    ```
## 🚀 Como Executar o Projeto

### 1. **Clone o Repositório**
```bash
git clone https://github.com/CamilaNunes7/crud_perfis_funcionarios.git
cd crud_perfis_funcionarios
```


### 2. **Crie o Ambiente Virtual**
```bash
python3 -m venv venv

# Se você utiliza Linux/MacOS, use:
source venv/bin/activate

# Se você utiliza Windows, use:
venv\Scripts\activate
```

### 3. **Instale as Dependências**
```bash
pip install -r requirements.txt
```

### 4. **Execute o Projeto**
```bash
uvicorn main:app --reload
```

O servidor estará disponível em: http://127.0.0.1:8000

---


## 🧪 Como Rodar os Testes
Execute os testes com o seguinte comando:

```bash
pytest tests/
