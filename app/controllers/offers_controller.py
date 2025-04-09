from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database.models.offers_db import get_all_vacancies

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

vacancy = get_all_vacancies()

@router.get("/offers", response_class=templates.TemplateResponse)
async def show_offers(request: Request):
    return templates.TemplateResponse("offers.html", {"request": request, "vacancy":vacancy })

