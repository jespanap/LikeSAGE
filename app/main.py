import os
from fastapi import FastAPI
from app.controllers import home, offers, login, register, profile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory="app/views/templates")

# http://127.0.0.1:8000
app.include_router(home.router)
# http://127.0.0.1:8000/offers
app.include_router(offers.router)
# http://127.0.0.1:8000/login
app.include_router(login.router)
# http://127.0.0.1:8000/register
app.include_router(register.router)
# http://127.0.0.1:8000/profile
app.include_router(profile.router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a Magneto"}

