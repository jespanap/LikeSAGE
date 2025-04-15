from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database.models.offers_db import get_all_vacancies
from fastapi.responses import HTMLResponse
from app.database.config.config import driver  # Asegúrate de tener acceso a `driver`
from app.utils import auth
from app.utils.auth import get_current_user


router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/offers", response_class=HTMLResponse)
async def show_offers(request: Request):
    user = auth.get_current_user(request) # 👈 extraemos el usuario de la sesión
    vacancies = get_all_vacancies()     # 👈 tu función para obtener vacantes

    return templates.TemplateResponse("offers.html", {
        "request": request,
        "vacancy": vacancies,
        "user": user  # 👈 muy importante que esto esté aquí
    })


@router.post("/offers/interact")
async def interact_with_offer(
    request: Request,
    titulo: str = Form(...),
    accion: str = Form(...)
):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    from app.models.offers import interact_with_vacancy
    interact_with_vacancy(user, titulo, accion)
    
    return RedirectResponse("/offers", status_code=303)


@router.post("/offers/like")
async def like_offer(request: Request, vacancy_title: str = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    with driver.session() as session:
        session.run("""
            MATCH (c:Candidate {correo: $correo}), (v:Vacancy {title: $title})
            MERGE (c)-[:LIKES]->(v)
        """, correo=user, title=vacancy_title)

    return RedirectResponse("/offers", status_code=303)


@router.post("/offers/save")
async def save_offer(request: Request, vacancy_title: str = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    with driver.session() as session:
        session.run("""
            MATCH (c:Candidate {correo: $correo}), (v:Vacancy {title: $title})
            MERGE (c)-[:SAVES]->(v)
        """, correo=user, title=vacancy_title)

    return RedirectResponse("/offers", status_code=303)


@router.post("/offers/share")
async def share_offer(request: Request, vacancy_title: str = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    with driver.session() as session:
        session.run("""
            MATCH (c:Candidate {correo: $correo}), (v:Vacancy {title: $title})
            MERGE (c)-[:SHARES]->(v)
        """, correo=user, title=vacancy_title)

    return RedirectResponse("/offers", status_code=303)
