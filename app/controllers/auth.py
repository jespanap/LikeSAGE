import json
import os
from fastapi import APIRouter, HTTPException, Form
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt 

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
USERS_FILE = "users.json"

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def cargar_usuarios():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as file:
        return json.load(file)

def guardar_usuarios(usuarios):
    with open(USERS_FILE, "w") as file:
        json.dump(usuarios, file, indent=2)

# Función para verificar la contraseña REVISARRRRRRRRRRRR
def verificar_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def crear_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    usuarios = cargar_usuarios()
    print("📄 Usuarios cargados desde JSON:", usuarios)  # DEBUG

    if not usuarios:
        print("⚠️ No se encontraron usuarios en users.json")
        raise HTTPException(status_code=500, detail="Error cargando usuarios")

    for usuario in usuarios:
        print(f"🔍 Comparando con usuario: {usuario['email']}")  # DEBUG
        print(f"🔑 Contraseña ingresada: {password}")  # DEBUG
        print(f"🔐 Hash almacenado: {usuario['password']}")  # DEBUG

        if verificar_password(password, usuario["password"]):
            print("✅ ¡Contraseña válida!")  # DEBUG
            token = crear_access_token({"sub": usuario["email"]})
            return {"access_token": token, "token_type": "bearer"}

    print("❌ Credenciales incorrectas")  # DEBUG
    raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
