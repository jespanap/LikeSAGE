from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
import json
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

USERS_FILE = "users.json"


# Función para cargar usuarios
def cargar_usuarios():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as file:
        return json.load(file)

# lo de joider
@router.get("/login", name="login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Procesar Formulario de Login
@router.post("/login")
async def login_usuario(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    usuarios = cargar_usuarios()

    for u in usuarios:
        if u["email"] == email and u["password"] == password:
            return templates.TemplateResponse("profile.html", {
                "request": request,
                "email": email,
                "message": "Inicio de sesión exitoso"
            })

    raise HTTPException(status_code=401, detail="Credenciales incorrectas")
