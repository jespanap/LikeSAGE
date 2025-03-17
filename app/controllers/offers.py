from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/offers", name="offers")
async def offers(request: Request):
    return templates.TemplateResponse("offers.html", {"request": request})
