from mysql.connector import Error
from fastapi import HTTPException
from app.database import get_db_connection
from typing import List, Dict

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

def create_sensor(tipo: str, token: str, id_recipiente: int):
    query = """
    INSERT INTO Sensores (tipo, token, id_recipiente)
    VALUES (%s, %s, %s)
    """
    values = (tipo, token, id_recipiente)

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        return {"tipo": tipo, "token": token, "id_recipiente": id_recipiente}
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

def create_ia_recipiente_sensor(id_sensor: int, valor: float, fecha: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # Obtener el id_recipiente correspondiente al id_sensor
        query_get_recipiente = "SELECT id_recipiente FROM Sensores WHERE id_sensor = %s"
        cursor.execute(query_get_recipiente, (id_sensor,))
        result = cursor.fetchone()
        
        if not result:
            return {"error": "No se encontró un recipiente asociado con el sensor proporcionado"}
        
        id_recipiente = result[0]

        # Insertar en IA_Recipiente_Sensor
        query_insert = """
        INSERT INTO IA_Recipiente_Sensor (id_recipiente, id_sensor, valor, fecha)
        VALUES (%s, %s, %s, %s)
        """
        values = (id_recipiente, id_sensor, valor, fecha)
        cursor.execute(query_insert, values)
        connection.commit()
        
        return {"id_recipiente": id_recipiente, "id_sensor": id_sensor, "valor": valor, "fecha": fecha}

    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
        return {"error": f"Error al insertar datos: {e}"}
    finally:
        cursor.close()
        connection.close()


def fetch_sensor_data(id_recipiente: int) -> List[Dict]:
    query = """
    SELECT 
        rs.valor, rs.fecha, s.tipo AS tipo_sensor, r.tipo AS tipo_recipiente,
        r.capacidad
    FROM 
        IA_Recipiente_Sensor rs
    INNER JOIN 
        Sensores s ON rs.id_sensor = s.id_sensor
    INNER JOIN 
        Recipientes r ON rs.id_recipiente = r.id_recipiente
    WHERE 
        rs.id_recipiente = %s
    ORDER BY 
        rs.fecha DESC
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, (id_recipiente,))
        data = cursor.fetchall()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {e}")
    finally:
        cursor.close()
        connection.close()

