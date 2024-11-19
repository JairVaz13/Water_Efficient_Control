from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_db_connection
from schemas.user import UserCreate
from schemas.container import ContainerCreate, ContainerUpdate
from schemas.sensor import SensorCreate, SensorUpdate, SensorData
from app.crud.user import create_user, authenticate_user  # Ajustado
from app.crud.containers import create_container, get_container, get_containers1, update_container, delete_container
from app.crud.sensors import create_sensor, get_Sensor, get_Sensores, update_sensor, delete_sensor, create_ia_recipiente_sensor, fetch_sensor_data
from pydantic import BaseModel
from sklearn.linear_model import LinearRegression
import numpy as np
import requests


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener la conexión a la base de datos
def get_db():
    db_connection = get_db_connection()
    try:
        yield db_connection
    finally:
        db_connection.close()

# Rutas para Usuarios
class LoginInput(BaseModel):
    email: str
    password: str

class LoginOutput(BaseModel):
    id_usuario: int
    nombre: str
    email: str
    token: str

# Crear usuario
@app.post("/user/crear", status_code=status.HTTP_200_OK, summary="Endpoint para registrarse", tags=['User'])
def create_user_endpoint(user: UserCreate):
    new_user = create_user(user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Error al crear el usuario")
    return new_user

# Iniciar sesión
@app.post("/login", status_code=status.HTTP_200_OK, summary="Endpoint para iniciar sesión", tags=['User'])
def login(user: LoginInput):
    authenticated_user = authenticate_user(user.email, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    return authenticated_user

# Rutas para Recipientes
@app.get("/containers/{token}", status_code=status.HTTP_200_OK, summary="Endpoint para obtener todos los Contenedores", tags=['Containers'])
def get_containers_endpoint(token: str):
    containers = get_containers1(token=token)
    if not containers:
        raise HTTPException(status_code=404, detail="No se encontraron contenedores")
    return containers

@app.get("/containers/{container_id}/{token}", status_code=status.HTTP_200_OK, summary="Endpoint para obtener un recipiente", tags=['Containers'])
def read_container(container_id: int, token: str):
    db_container = get_container(container_id=container_id, token=token)
    if db_container is None:
        raise HTTPException(status_code=404, detail="Container not found")
    return db_container

@app.post("/containers/crear", status_code=status.HTTP_201_CREATED, summary="Endpoint para crear un recipiente", tags=['Containers'])
def create_container_endpoint(container: ContainerCreate):
    ubicacion = container.ubicacion
    tipo = container.tipo
    capacidad = container.capacidad
    token = container.token
    
    new_container = create_container(ubicacion, tipo, capacidad, token)
    return new_container

@app.put("/containers/{container_id}/{token}", status_code=status.HTTP_200_OK, summary="Endpoint para actualizar un recipiente", tags=['Containers'])
def update_container_endpoint(container_id: int, token: str, container: ContainerUpdate):
    db_container = update_container(container_id=container_id, token=token, 
                                    ubicacion=container.ubicacion, tipo=container.tipo, 
                                    capacidad=container.capacidad)    
    if db_container is None:
        raise HTTPException(status_code=404, detail="Container not found")
    return db_container


@app.delete("/containers/{container_id}/{token}", status_code=status.HTTP_200_OK, summary="Endpoint para eliminar un recipiente", tags=['Containers'])
def delete_container_endpoint(container_id: int, token: str):
    db_container = delete_container(container_id, token)
    if db_container is None:
        raise HTTPException(status_code=404, detail="Container not found")
    return db_container

# Rutas para Sensores
@app.get("/sensors/{token}", status_code=status.HTTP_200_OK, summary="Endpoint para obtener todos los sensores", tags=['Sensors'])
def get_sensors_endpoint(token: str):
    sensors = get_Sensores(token=token)
    if not sensors:
        raise HTTPException(status_code=404, detail="No se encontraron contenedores")
    return sensors

@app.post("/sensors/crear", status_code=status.HTTP_201_CREATED, summary="Endpoint para crear un sensor", tags=['Sensors'])
def create_sensor_endpoint(sensor: SensorCreate):
    tipo = sensor.tipo
    token = sensor.token
    new_sensor = create_sensor(tipo, token)
    return new_sensor

@app.get("/sensors/{sensor_id}/{token}", status_code=status.HTTP_200_OK, summary="Endpoint para obtener un sensor", tags=['Sensors'])
def read_sensor(sensor_id: int, token: str):
    db_sensor = get_Sensor(sensor_id=sensor_id, token=token)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor

@app.put("/sensors/{sensor_id}/{token}", status_code=status.HTTP_200_OK, summary="Endpoint para actualizar un sensor", tags=['Sensors'])
def update_sensor_endpoint(sensor_id: int, token: str, sensor: SensorUpdate):
    db_sensor = update_sensor(sensor_id=sensor_id, token=token, tipo=sensor.tipo)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor

@app.delete("/sensors/{sensor_id}/{token}", status_code=status.HTTP_200_OK, summary="Endpoint para eliminar un sensor", tags=['Sensors'])
def delete_sensor_endpoint(sensor_id: int, token: str):
    db_sensor = delete_sensor(sensor_id, token)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor

# Rutas para IA Recipiente Sensor
@app.post("/ia_recipiente_sensor/crear", status_code=status.HTTP_201_CREATED, summary="Endpoint para crear un registro de sensor", tags=['IA Recipiente Sensor'])
def create_ia_recipiente_sensor_endpoint(id_recipiente: int, id_sensor: int, valor: float, fecha: str):
    new_ia_recipiente_sensor = create_ia_recipiente_sensor(id_recipiente, id_sensor, valor, fecha)
    return new_ia_recipiente_sensor


@app.get("/ia/recommendations", summary="Obtener recomendaciones basadas en datos de sensores", tags=["IA Recipiente Sensor"])
def generate_recommendations_with_ollama_endpoint(
    id_recipiente: int = Query(..., description="ID del recipiente para generar recomendaciones")
):
    try:
        # 1. Obtener datos
        data = fetch_sensor_data(id_recipiente)
        if not data:
            raise HTTPException(status_code=404, detail="No se encontraron datos para este recipiente")
        
        # 2. Procesar datos - con verificación
        try:
            valores = np.array([row[0] for row in data]).reshape(-1, 1)
            if len(valores) == 0:
                raise ValueError("No hay valores válidos para procesar")
        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Error al procesar los datos del sensor: {str(e)}"
            )

        # 3. Entrenar modelo
        try:
            fechas = np.arange(len(valores)).reshape(-1, 1)
            model = LinearRegression()
            model.fit(fechas, valores)
            predicciones = model.predict(fechas)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error en el procesamiento del modelo: {str(e)}"
            )

        # 4. Preparar mensaje
        promedio = np.mean(valores)
        mensaje = f"""
        Tengo datos de sensores para un recipiente. El promedio actual de TDS/pH/temperatura es {promedio:.2f}.
        Proporciona recomendaciones específicas para mejorar la calidad basadas en estándares internacionales.
        """

        # 5. Llamada a Ollama con timeout
        try:
            response = requests.post(
                "http://localhost:11500/api/generate",
                json={
                    "model": "qwen2.5-coder:0.5b",
                    "prompt": mensaje
                },
                timeout=10  # timeout de 10 segundos
            )
            response.raise_for_status()  # Lanza excepción si status_code != 2xx
            recomendacion = response.json().get("response", "No se recibieron recomendaciones.")
        except requests.exceptions.ConnectionError:
            raise HTTPException(
                status_code=503,
                detail="No se pudo conectar al servicio de Ollama. Verifica que esté corriendo."
            )
        except requests.exceptions.Timeout:
            raise HTTPException(
                status_code=504,
                detail="Timeout al conectar con Ollama"
            )
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al comunicarse con Ollama: {str(e)}"
            )

        # 6. Retornar resultados
        return {
            "promedio": float(promedio),
            "predicciones": predicciones.tolist(),
            "recomendaciones": recomendacion
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )