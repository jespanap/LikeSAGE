from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_ingresada = "06160921"
password_guardada = "$2b$12$dgnXsX2CQn.QlVCIIJSgF.lqTx7UN2HEB9vb9qdUDNdu/OlJv6EQG"
resultado = pwd_context.verify(password_ingresada, password_guardada)

print(f"✅ Coincide: {resultado}")
