from mysql.connector import Error
from ..database import get_db_connection

# Obtener todos los dispensadores
def get_dispensadores(token: str):
    query = "SELECT * FROM Dispensador WHERE token = %s"    
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

# Obtener un dispensador por ID
def get_dispensador(dispensador_id: int, token: str):
    query = "SELECT * FROM Dispensador WHERE id_dispensador = %s AND token = %s"
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, (dispensador_id, token))
        return cursor.fetchone()
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

# Crear un dispensador
def create_dispensador(estado: str, id_recipiente: int, token: str):    
    query = """
    INSERT INTO Dispensador (estado, id_recipiente, token)
    VALUES (%s, %s, %s)
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, (estado, id_recipiente, token))
        connection.commit()
        return {"estado": estado, "id_recipiente": id_recipiente, "token": token}
    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def update_dispensador(dispensador_id: int, estado: str, token: str):
    query_check = """
    SELECT id_dispensador FROM Dispensador WHERE id_dispensador = %s AND token = %s
    """
    query_update_state = """
    UPDATE Dispensador SET estado = %s WHERE id_dispensador = %s AND token = %s
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # Verificar si el dispensador existe
        cursor.execute(query_check, (dispensador_id, token))
        if not cursor.fetchone():
            return {"error": "Dispensador no encontrado"}

        # Actualizar el estado del dispensador
        cursor.execute(query_update_state, (estado, dispensador_id, token))
        connection.commit()

        if cursor.rowcount == 0:  # Verificar si se afectaron filas
            return {"error": "No se pudo actualizar el dispensador"}

        return {"id_dispensador": dispensador_id, "estado": estado, "token": token}

    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
        return {"error": f"Error en la base de datos: {e}"}
    finally:
        cursor.close()
        connection.close()

# Eliminar un dispensador
def delete_dispensador(dispensador_id: int, token: str):
    query = "DELETE FROM Dispensador WHERE id_dispensador = %s AND token = %s"
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, (dispensador_id, token))
        connection.commit()
        return {"message": "Dispensador eliminado correctamente"}
    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
