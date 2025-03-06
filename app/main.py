from fastapi import FastAPI
from app.controllers import home, offers

app = FastAPI()

# http://127.0.0.1:8000
app.include_router(home.router)
# http://127.0.0.1:8000/offers
app.include_router(offers.router)
