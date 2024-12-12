from fastapi import FastAPI, Depends, HTTPException, status, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_db_connection
from schemas.user import UserCreate
from schemas.container import ContainerCreate, ContainerUpdate
from schemas.sensor import SensorCreate, SensorUpdate, SensorData
from schemas.dispensador import DispensadorCreate, DispensadorUpdate
from app.crud.user import create_user, authenticate_user
from app.crud.containers import create_container, get_container, get_containers1, update_container, delete_container
from app.crud.sensors import create_sensor, get_Sensor, get_Sensores, update_sensor, delete_sensor, create_ia_recipiente_sensor, fetch_sensor_data
from app.crud.dispensador import (create_dispensador, get_dispensador, get_dispensadores, update_dispensador, delete_dispensador,)
from sklearn.linear_model import LinearRegression
from fastapi.responses import JSONResponse
import google.generativeai as genai
from datetime import timedelta
from pydantic import BaseModel
import base64
import numpy as np
import requests
import os


# Configuración de la API de Gemini
API_KEY = 'AIzaSyA9uKfw3cv-1HOmic_ff7nLlFvq3yj7tyo'
genai.configure(api_key=API_KEY)

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
    id_recipiente = sensor.id_recipiente
    new_sensor = create_sensor(tipo, token, id_recipiente)
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
def create_ia_recipiente_sensor_endpoint(id_sensor: int, valor: float, fecha: str):
    new_ia_recipiente_sensor = create_ia_recipiente_sensor(id_sensor, valor, fecha)
    return new_ia_recipiente_sensor

@app.get("/ia/recommendations", summary="Obtener recomendaciones basadas en datos de sensores", tags=["IA Recipiente Sensor"])
def generate_recommendations(
    id_recipiente: int = Query(..., description="ID del recipiente para generar recomendaciones")
):
    try:
        # 1. Obtener datos de la base de datos
        sensor_data = fetch_sensor_data(id_recipiente)
        if not sensor_data:
            raise HTTPException(status_code=404, detail="No se encontraron datos para este recipiente")
        
        # 2. Verificar que los datos contienen las claves necesarias
        tipo_recipiente = sensor_data[0].get("tipo_recipiente")
        capacidad_recipiente = sensor_data[0].get("capacidad")
        
        if tipo_recipiente is None or capacidad_recipiente is None:
            raise HTTPException(status_code=500, detail="Faltan datos de tipo o capacidad del recipiente")

        # 3. Agrupar los datos por tipo de sensor
        sensores = {}
        for row in sensor_data:
            tipo_sensor = row["tipo_sensor"]
            if tipo_sensor not in sensores:
                sensores[tipo_sensor] = []
            sensores[tipo_sensor].append(row)
        
        # 4. Preparar y procesar predicciones para cada sensor
        resultado = []
        dias_prediccion = 3  
        for tipo_sensor, sensor_data in sensores.items():
            try:
                fechas = np.array([row["fecha"] for row in sensor_data])  
                valores = np.array([row["valor"] for row in sensor_data]).reshape(-1, 1)
                if len(valores) == 0:
                    raise ValueError(f"No hay valores válidos para el sensor {tipo_sensor}")
                
                dias = np.array([(fecha - fechas[0]).days for fecha in fechas]).reshape(-1, 1)
                model = LinearRegression()
                model.fit(dias, valores)
                
                dias_pred = np.array([dias.max() + i for i in range(1, dias_prediccion + 1)]).reshape(-1, 1)
                predicciones = model.predict(dias_pred)
                
                datos_sensor = [
                    {"fecha": fecha.strftime("%Y-%m-%d"), "valor": float(valores[i][0])}
                    for i, fecha in enumerate(fechas)
                ]
                datos_predicciones = [
                    {"fecha": (fechas[-1] + timedelta(days=i)).strftime("%Y-%m-%d"), "valor_predicho": float(pred[0])}
                    for i, pred in enumerate(predicciones, start=1)
                ]
                
                resultado.append({
                    "tipo_sensor": tipo_sensor,
                    "datos_sensor": datos_sensor + datos_sensor,  
                    "predicciones": datos_predicciones + datos_predicciones 
                })
            
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error al procesar los datos para el sensor {tipo_sensor}: {str(e)}"
                )

        # 5. Formatear el payload para la API externa, incorporando la información del recipiente
        payload = {
            "id_recipiente": id_recipiente,
            "tipo_recipiente": tipo_recipiente,
            "capacidad_recipiente": capacidad_recipiente,
            "sensores": resultado
        }

        print(payload)
        
        # 6. Enviar los datos a la API externa
        url = "https://magicloops.dev/api/loop/97e29a29-1da2-42d0-a963-96cf0b5ef88a/run"
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error al enviar los datos: {response.text}"
            )
        
        return {"tipo_recipiente": tipo_recipiente,
            "capacidad_recipiente": capacidad_recipiente,
            "sensores": resultado, "response": response.json()}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@app.post("/ia/foto", status_code=status.HTTP_200_OK, summary="Analizar imagen y generar recomendaciones", tags=["IA Recipiente Sensor"])
async def foto_analisis(
    id_recipiente: int = Query(..., description="ID del recipiente para generar recomendaciones"),
    file: UploadFile = File(..., description="Imagen a analizar")
):
    try:
        # 1. Obtener datos del recipiente
        sensor_data = fetch_sensor_data(id_recipiente)
        if not sensor_data:
            raise HTTPException(status_code=404, detail="No se encontraron datos para este recipiente")
        
        tipo_recipiente = sensor_data[0].get("tipo_recipiente")
        capacidad_recipiente = sensor_data[0].get("capacidad")
        if not tipo_recipiente or not capacidad_recipiente:
            raise HTTPException(status_code=500, detail="Datos incompletos del recipiente")

        # 2. Procesar datos de sensores
        sensores = {}
        for row in sensor_data:
            tipo_sensor = row["tipo_sensor"]
            if tipo_sensor not in sensores:
                sensores[tipo_sensor] = []
            sensores[tipo_sensor].append(row)

        resultado_sensores = []
        dias_prediccion = 3
        for tipo_sensor, sensor_data in sensores.items():
            fechas = np.array([row["fecha"] for row in sensor_data], dtype='datetime64')
            valores = np.array([row["valor"] for row in sensor_data]).reshape(-1, 1)
            if len(valores) == 0:
                continue
            
            dias = np.array([(fecha - fechas[0]).astype(int) for fecha in fechas]).reshape(-1, 1)
            model = LinearRegression()
            model.fit(dias, valores)
            
            dias_pred = np.array([dias.max() + i for i in range(1, dias_prediccion + 1)]).reshape(-1, 1)
            predicciones = model.predict(dias_pred)
            
            datos_sensor = [
                {"fecha": str(fechas[i]), "valor": float(valores[i][0])}
                for i in range(len(valores))
            ]
            datos_predicciones = [
                {"fecha": str((fechas[-1] + np.timedelta64(i, 'D'))), "valor_predicho": float(pred[0])}
                for i, pred in enumerate(predicciones, start=1)
            ]
            
            resultado_sensores.append({
                "tipo_sensor": tipo_sensor,
                "datos_sensor": datos_sensor,
                "predicciones": datos_predicciones
            })

        # 3. Analizar imagen usando Gemini
        try:
            temp_file_path = f"/tmp/{file.filename}"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(await file.read())
            
            uploaded_file = genai.upload_file(temp_file_path)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([
                f"Describe el estado del agua en esta imagen, identifica colores, posibles contaminantes y recomienda acciones específicas(como cuanto usar de cloro o algun otro prtoducto quimico y en que proporciones segun el {tipo_recipiente} y su cpacidad {capacidad_recipiente}). recuerda debes responder asi (Como tu IA generativa para tu {tipo_recipiente} que tiene esta capicidad {capacidad_recipiente} )",
                uploaded_file
            ])
            
            os.remove(temp_file_path)  # Limpieza del archivo temporal

            analisis_imagen = {
                "estado_agua": response.text,
            }
            

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en el análisis de la imagen: {str(e)}")

        # 4. Generar respuesta final
        return JSONResponse(content={
            "id_recipiente": id_recipiente,
            "tipo_recipiente": tipo_recipiente,
            "capacidad_recipiente": capacidad_recipiente,
            "analisis_sensores": resultado_sensores,
            "analisis_imagen": analisis_imagen
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el análisis: {str(e)}")



@app.post("/ia/foto/base", status_code=status.HTTP_200_OK, summary="Analizar imagen y generar recomendaciones", tags=["IA Recipiente Sensor"])
async def foto_analisis(
    id_recipiente: int = Query(..., description="ID del recipiente para generar recomendaciones"),
    file_base64: str = Query(..., description="Imagen en formato Base64 a analizar")
):
    try:
        # 1. Obtener datos del recipiente
        sensor_data = fetch_sensor_data(id_recipiente)
        if not sensor_data:
            raise HTTPException(status_code=404, detail="No se encontraron datos para este recipiente")
        
        tipo_recipiente = sensor_data[0].get("tipo_recipiente")
        capacidad_recipiente = sensor_data[0].get("capacidad")
        if not tipo_recipiente or not capacidad_recipiente:
            raise HTTPException(status_code=500, detail="Datos incompletos del recipiente")

        # 2. Procesar datos de sensores
        sensores = {}
        for row in sensor_data:
            tipo_sensor = row["tipo_sensor"]
            if tipo_sensor not in sensores:
                sensores[tipo_sensor] = []
            sensores[tipo_sensor].append(row)

        resultado_sensores = []
        dias_prediccion = 3
        for tipo_sensor, sensor_data in sensores.items():
            fechas = np.array([row["fecha"] for row in sensor_data], dtype='datetime64')
            valores = np.array([row["valor"] for row in sensor_data]).reshape(-1, 1)
            if len(valores) == 0:
                continue
            
            dias = np.array([(fecha - fechas[0]).astype(int) for fecha in fechas]).reshape(-1, 1)
            model = LinearRegression()
            model.fit(dias, valores)
            
            dias_pred = np.array([dias.max() + i for i in range(1, dias_prediccion + 1)]).reshape(-1, 1)
            predicciones = model.predict(dias_pred)
            
            datos_sensor = [
                {"fecha": str(fechas[i]), "valor": float(valores[i][0])}
                for i in range(len(valores))
            ]
            datos_predicciones = [
                {"fecha": str((fechas[-1] + np.timedelta64(i, 'D'))), "valor_predicho": float(pred[0])}
                for i, pred in enumerate(predicciones, start=1)
            ]
            
            resultado_sensores.append({
                "tipo_sensor": tipo_sensor,
                "datos_sensor": datos_sensor,
                "predicciones": datos_predicciones
            })

        # 3. Analizar imagen usando Gemini
        try:
            # Decodificar Base64
            temp_file_path = "/tmp/temp_image.jpg"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(base64.b64decode(file_base64))
            
            uploaded_file = genai.upload_file(temp_file_path)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([
                f"Describe el estado del agua en esta imagen, identifica colores, posibles contaminantes y recomienda acciones específicas(como cuanto usar de cloro o algun otro prtoducto quimico y en que proporciones segun el {tipo_recipiente} y su cpacidad {capacidad_recipiente}). recuerda debes responder asi (Como tu IA generativa para tu {tipo_recipiente} que tiene esta capicidad {capacidad_recipiente} )",
                uploaded_file
            ])
            
            os.remove(temp_file_path)  # Limpieza del archivo temporal

            analisis_imagen = {
                "estado_agua": response.text,
            }
            

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en el análisis de la imagen: {str(e)}")

        # 4. Generar respuesta final
        return JSONResponse(content={
            "id_recipiente": id_recipiente,
            "tipo_recipiente": tipo_recipiente,
            "capacidad_recipiente": capacidad_recipiente,
            "analisis_sensores": resultado_sensores,
            "analisis_imagen": analisis_imagen
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el análisis: {str(e)}")

#Rutas para Dispensador
@app.get("/dispensadores", status_code=status.HTTP_200_OK, summary="Obtener todos los dispensadores", tags=['Dispensadores'])
def get_all_dispensadores(token: str):
    dispensadores = get_dispensadores(token)
    if not dispensadores:
        raise HTTPException(status_code=404, detail="No se encontraron dispensadores")
    return dispensadores

# Obtener un dispensador por ID
@app.get("/dispensadores/{dispensador_id}", status_code=status.HTTP_200_OK, summary="Obtener un dispensador por ID", tags=['Dispensadores'])
def get_dispensador_by_id(dispensador_id: int, token: str):
    dispensador = get_dispensador(dispensador_id, token)
    if not dispensador:
        raise HTTPException(status_code=404, detail="Dispensador no encontrado")
    return dispensador

# Crear un nuevo dispensador
@app.post("/dispensadores/crear", status_code=status.HTTP_201_CREATED, summary="Crear un dispensador", tags=['Dispensadores'])
def create_dispensador_endpoint(dispensador: DispensadorCreate):
    new_dispensador = create_dispensador(dispensador.estado, dispensador.id_recipiente, dispensador.token)
    if not new_dispensador:
        raise HTTPException(status_code=400, detail="Error al crear el dispensador")
    return new_dispensador

# Endpoint para actualizar un dispensador
@app.patch("/dispensadores/{dispensador_id}", status_code=status.HTTP_200_OK, summary="Actualizar un dispensador", tags=['Dispensadores'])
def update_dispensador_endpoint(dispensador_id: int, dispensador: DispensadorUpdate):
    updated_dispensador = update_dispensador(dispensador_id, dispensador.estado, dispensador.token)
    if not updated_dispensador:
        raise HTTPException(status_code=404, detail="Dispensador no encontrado o no se pudo actualizar")
    return updated_dispensador

# Eliminar un dispensador
@app.delete("/dispensadores/{dispensador_id}", status_code=status.HTTP_200_OK, summary="Eliminar un dispensador", tags=['Dispensadores'])
def delete_dispensador_endpoint(dispensador_id: int, token: str):
    deleted_dispensador = delete_dispensador(dispensador_id, token)
    if not deleted_dispensador:
        raise HTTPException(status_code=404, detail="Dispensador no encontrado")
    return deleted_dispensador  

# Rutas para Graficos y notificaciones
@app.get("/graficos", status_code=status.HTTP_200_OK, summary="Endpoint para obtener los datos para gráficos", tags=['Graficos y notificaiones'])
def get_graph_data(token: str):
    # Obtener id del trcipiente segun el token
    id_recipiente = get_containers1(token=token)[0].get("id_recipiente")

    # Obtener datos de sensores
    sensor_data = fetch_sensor_data(id_recipiente)
    if not sensor_data:
        raise HTTPException(status_code=404, detail="No se encontraron datos para este recipiente")
    
    # Procesar datos de sensores
    sensores = {}

    for row in sensor_data:
        tipo_sensor = row["tipo_sensor"]
        if tipo_sensor not in sensores:
            sensores[tipo_sensor] = []
        sensores[tipo_sensor].append(row)

    resultado_sensores = []

    for tipo_sensor, sensor_data in sensores.items():

        fechas = np.array([row["fecha"] for row in sensor_data], dtype='datetime64')
        valores = np.array([row["valor"] for row in sensor_data]).reshape(-1, 1)
        if len(valores) == 0:
            continue
        
        dias = np.array([(fecha - fechas[0]).astype(int) for fecha in fechas]).reshape(-1, 1)
        model = LinearRegression()
        model.fit(dias, valores)
        
        datos_sensor = [
            {"fecha": str(fechas[i]), "valor": float(valores[i][0])}
            for i in range(len(valores))
        ]
        
        resultado_sensores.append({
            "tipo_sensor": tipo_sensor,
            "datos_sensor": datos_sensor,
        })
    
    return resultado_sensores