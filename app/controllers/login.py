from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
