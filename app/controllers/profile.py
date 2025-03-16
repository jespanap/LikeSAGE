from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/profile")
async def profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})
