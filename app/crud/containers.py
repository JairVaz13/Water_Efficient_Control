from mysql.connector import Error
from ..database import get_db_connection


def get_containers1(token: str):
    query = "SELECT * FROM Recipientes WHERE token = %s"
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, (token,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def get_container(container_id: int, token: str):
    query = "SELECT * FROM Recipientes WHERE id_recipiente = %s AND token = %s"
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, (container_id, token,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()


def create_container(ubicacion: str, tipo: str, capacidad: int, token: str):
    query = """
    INSERT INTO Recipientes (ubicacion, tipo, capacidad, token)
    VALUES (%s, %s, %s, %s)
    """
    values = (ubicacion, tipo, capacidad, token)

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Recipiente creado correctamente.")
        return {"ubicacion": ubicacion, "tipo": tipo, "capacidad": capacidad}
    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


def update_container(container_id: int, token: str, ubicacion: str, tipo: str, capacidad: int):
    query = """
    UPDATE Recipientes SET ubicacion = %s, tipo = %s, capacidad = %s
    WHERE id_recipiente = %s AND token = %s
    """
    values = (ubicacion, tipo, capacidad, container_id, token)

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        return {"ubicacion": ubicacion, "tipo": tipo, "capacidad": capacidad}
    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def delete_container(container_id: int, token: str):
    query = "DELETE FROM Recipientes WHERE id_recipiente = %s AND token = %s"
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, (container_id, token))
        connection.commit()
        return {"message": "Container eliminado correctamente"}
    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
