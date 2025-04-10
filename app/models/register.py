from passlib.context import CryptContext
from app.database.config.config import driver  # Ajusta si tienes otra ruta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(correo: str, password: str) -> bool:
    hashed_password = pwd_context.hash(password)

    with driver.session() as session:
        # Verifica si ya existe el correo
        result = session.run("MATCH (c:Candidate {correo: $correo}) RETURN c", correo=correo)
        if result.single():
            return False  # Ya hay un usuario con ese correo

        # Crea nodo Candidate
        session.run(
            """
            CREATE (c:Candidate {
                correo: $correo,
                password: $password
            })
            """,
            correo=correo,
            password=hashed_password
        )
        return True
