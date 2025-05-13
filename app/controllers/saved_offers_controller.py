from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database.config.config import driver
from app.utils.auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/saved-offers", response_class=HTMLResponse)
async def show_saved_offers(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    with driver.session() as session:
        results = session.run("""
            MATCH (c:Candidate {correo: $correo})-[s:SAVES]->(v:Vacancy)
                              OPTIONAL MATCH (c)-[l:LIKES]->(v)
            RETURN v.title AS titulo, s.timestamp AS saved_time
            ORDER BY saved_time DESC
        """, correo=user)

        saved_vacancies = []
        for record in results:
            saved_vacancies.append({
                "titulo": record["titulo"],
                "liked": True,   # puedes adaptarlo según lógica real
                "saved": True
            })

    return templates.TemplateResponse("saved_offers.html", {
        "request": request,
        "user": user,
        "vacancy": saved_vacancies,
        "page": 1,
        "total_pages": 1,
        "query": None
    })
