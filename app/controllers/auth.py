from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, User
from app.utils.auth import verify_password, create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
async def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
