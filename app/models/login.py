import json
from passlib.context import CryptContext
from pathlib import Path

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
USERS_FILE = Path("app/data/users.json")

def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def authenticate_user(username: str, password: str):
    users = load_users()
    user = users.get(username)

    if isinstance(user, str):
        print(f"[ERROR] Usuario '{username}' tiene un valor string en vez de un dict. Revisa tu users.json.")
        return None

    if user and pwd_context.verify(password, user["password"]):
        return {"username": username}
    return None
