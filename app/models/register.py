import json
import os
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
USERS_FILE = "app/data/users.json"

def register_user(username: str, password: str) -> bool:
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    else:
        users = {}

    if username in users:
        return False

    users[username] = {
        "password": pwd_context.hash(password)
    }

    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

    return True
