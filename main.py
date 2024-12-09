from fastapi import FastAPI, HTTPException, Query, UploadFile, File, status
from fastapi.responses import JSONResponse
from sklearn.linear_model import LinearRegression
from datetime import timedelta
import numpy as np
import google.generativeai as genai
import os

# Configuración de la API de Gemini
API_KEY = 'AIzaSyAhRae2tesr51ZghpECc5AqU4bZon9cuQg'
genai.configure(api_key=API_KEY)

app = FastAPI()

# Simulación de la función para obtener datos del sensor
def fetch_sensor_data(id_recipiente: int):
    # Reemplaza esta función con una conexión real a la base de datos
    return [
        {"tipo_recipiente": "Tanque", "capacidad": 1000, "tipo_sensor": "pH", "fecha": "2024-12-01", "valor": 7.5},
        {"tipo_recipiente": "Tanque", "capacidad": 1000, "tipo_sensor": "pH", "fecha": "2024-12-02", "valor": 7.4},
    ]

@app.post("/ia/foto", status_code=status.HTTP_200_OK, summary="Analizar imagen y generar recomendaciones")
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
