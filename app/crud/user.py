from app.database import get_db_connection
from schemas.user import UserCreate
from mysql.connector import Error
import bcrypt
import uuid

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user(user: UserCreate):
    hashed_password = get_password_hash(user.contrasena)
    token = str(uuid.uuid4())  # Generar un token único aleatorio
    query = """
    INSERT INTO Usuarios (nombre, email, contrasena, token)
    VALUES (%s, %s, %s, %s)
    """
    values = (user.nombre, user.email, hashed_password, token)

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        user_id = cursor.lastrowid
        return {"id_usuario": user_id, "nombre": user.nombre, "email": user.email, "token": token}
    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def authenticate_user(email: str, password: str):
    query = "SELECT id_usuario, nombre, email, contrasena, token FROM Usuarios WHERE email = %s"
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        if user and verify_password(password, user["contrasena"]):
            return {
                "id_usuario": user["id_usuario"],
                "nombre": user["nombre"],
                "email": user["email"],
                "token": user["token"]
            }
        return None
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
