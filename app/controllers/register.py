from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, Field

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

class RegisterRequest(BaseModel):
    nombre: str = Field(..., min_length=2, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    edad: int = Field(..., ge=1, description="Edad debe ser un número positivo")
    password: str = Field(..., min_length=6, description="Contraseña mínima de 6 caracteres")

@router.post("/register")
async def register(
    nombre: str = Form(...),
    email: str = Form(...),
    edad: int = Form(...),
    password: str = Form(...)
):
    if not (nombre and email and edad and password):
        raise HTTPException(status_code=400, detail="Todos los campos son obligatorios.")

    if edad < 1:
        raise HTTPException(status_code=400, detail="La edad debe ser mayor a 0.")

    return JSONResponse(content={"success": True, "message": "Registro exitoso."}, status_code=201)

@router.get("/register", name="register")
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
