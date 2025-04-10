from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.models import register
from app.utils.auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/register")
async def show_register_form(request: Request):
    if get_current_user(request):
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def do_register(
    request: Request,
    correo: str = Form(...),
    password: str = Form(...)
):
    if get_current_user(request):
        return RedirectResponse("/", status_code=303)

    success = register.register_user(correo, password)
    if success:
        return RedirectResponse("/login", status_code=303)
    else:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "El correo ya está registrado"
        })

