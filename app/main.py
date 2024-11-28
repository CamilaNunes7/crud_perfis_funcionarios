from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, user

# Inicializa as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Rotas
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/users", tags=["Users"])

