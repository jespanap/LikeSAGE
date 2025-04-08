from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse
from app.controllers import login_controller, register_controller
from app.utils import auth

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="TU_SECRETO_AQUI")
templates = Jinja2Templates(directory="app/views/templates")

app.include_router(login_controller.router)
app.include_router(register_controller.router)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    user = auth.get_current_user(request)
    return templates.TemplateResponse("home.html", {"request": request, "user": user})
