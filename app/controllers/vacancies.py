from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/vacancies")
async def vacancies(request: Request):
    return templates.TemplateResponse("vacancies.html", {"request": request})
