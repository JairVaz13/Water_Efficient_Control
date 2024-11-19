from mysql.connector import Error
from fastapi import HTTPException
from app.database import get_db_connection

def get_Sensores(token: str):
    query = "SELECT * FROM Sensores WHERE token = %s"
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

def get_Sensor(sensor_id: int, token: str):
    query = "SELECT * FROM Sensores WHERE id_sensor = %s AND token = %s"
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, (sensor_id, token,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def create_sensor(tipo: str, token: str):
    query = """
    INSERT INTO Sensores (tipo, token)
    VALUES (%s, %s)
    """
    values = (tipo, token)

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        return {"tipo": tipo}
    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

def update_sensor(sensor_id: int, token: str, tipo: str):
    query = """
    UPDATE Sensores SET tipo = %s
    WHERE id_sensor = %s AND token = %s
    """
    values = (tipo, sensor_id, token)

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        return {"id_sensor": sensor_id, "tipo": tipo}
    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def delete_sensor(sensor_id: int, token: str):
    query = "DELETE FROM Sensores WHERE id_sensor = %s AND token = %s"
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, (sensor_id, token))
        connection.commit()
        return {"message": "Sensor eliminado correctamente"}
    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def create_ia_recipiente_sensor(id_recipiente: int, id_sensor: int, valor: float, fecha: str):
    query = """
    INSERT INTO IA_Recipiente_Sensor (id_recipiente, id_sensor, valor, fecha)
    VALUES (%s, %s, %s, %s)
    """
    values = (id_recipiente, id_sensor, valor, fecha)
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        return {"id_recipiente": id_recipiente, "id_sensor": id_sensor, "valor": valor, "fecha": fecha}
    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def fetch_sensor_data(id_recipiente: int):
    query = """
    SELECT valor, fecha, id_sensor FROM IA_Recipiente_Sensor
    WHERE id_recipiente = %s
    ORDER BY fecha DESC
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, (id_recipiente,))
        data = cursor.fetchall()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {e}")
    finally:
        cursor.close()
        connection.close()