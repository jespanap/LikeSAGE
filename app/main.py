from fastapi import FastAPI, HTTPException, Depends
from app.controllers import home, offers, login, register, profile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, Field
import json
import os
from passlib.context import CryptContext

app = FastAPI()
USERS_FILE = "users.json"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Contraseña mínima de 6 caracteres")

def cargar_usuarios():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def guardar_usuarios(usuarios):
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(usuarios, file, indent=2)

@app.post("/register", status_code=201)
async def register_user(user: UserRegister):
    usuarios = cargar_usuarios()

    if any(u["email"] == user.email for u in usuarios):
        raise HTTPException(status_code=400, detail="El usuario ya está registrado.")

    hashed_password = pwd_context.hash(user.password)  
    nuevo_usuario = {"email": user.email, "password": hashed_password}

    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)

    return {"message": "Usuario registrado exitosamente."}

@app.get("/health")
def health_check():
    return {"message": "FastAPI está corriendo correctamente."}

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/views/templates")

# http://127.0.0.1:8000/
app.include_router(home.router)
# http://127.0.0.1:8000/offers
app.include_router(offers.router)
# http://127.0.0.1:8000/login
app.include_router(login.router)
# http://127.0.0.1:8000/register
app.include_router(register.router)
# http://127.0.0.1:8000/profile
app.include_router(profile.router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a Magneto"}
