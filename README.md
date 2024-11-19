# Water Efficient Control

Una API para administrar recipientes y sensores de manera eficiente, incorporando inteligencia artificial para proporcionar recomendaciones basadas en datos.

---

## 📌 Tabla de Contenidos

- [URL de la API](#-url-de-la-api)
- [Ejecución Local](#-ejecución-local)
- [Endpoints](#-endpoints)
  - [Usuarios](#-usuarios)
  - [Recipientes](#-recipientes)
  - [Sensores](#-sensores)
  - [IA](#-ia)
- [Contribuir](#-contribuir)

---

## 🌐 URL de la API

La API está desplegada en [Render](https://water-efficient-control.onrender.com/).

---

## 💻 Ejecución Local

Usa el siguiente comando para ejecutar la API en un entorno local:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📂 Endpoints

---

    Usuarios
    POST /user/crear
    Registro de nuevos usuarios.
    Cuerpo de solicitud:

    json
    Copiar código
    {
    "username": "example",
    "password": "12345"
    }
    POST /login
    Autenticación de usuarios registrados.

    Recipientes
    GET /containers/{token}
    Obtén todos los recipientes.

    GET /containers/{container_id}/{token}
    Obtén información de un recipiente específico.

    POST /containers/crear
    Crea un nuevo recipiente.
    Cuerpo de solicitud:

    json
    Copiar código
    {
    "name": "Recipiente 1",
    "capacity": 100
    }
    PUT /containers/{container_id}/{token}
    Actualiza la información de un recipiente.

    DELETE /containers/{container_id}/{token}
    Elimina un recipiente existente.

    Sensores
    GET /sensors/{token}
    Obtén todos los sensores registrados.

    POST /sensors/crear
    Registra un nuevo sensor.
    Cuerpo de solicitud:

    json
    Copiar código
    {
    "name": "Sensor 1",
    "type": "temperature"
    }
    GET /sensors/{sensor_id}/{token}
    Obtén detalles de un sensor.

    PUT /sensors/{sensor_id}/{token}
    Actualiza un sensor existente.

    DELETE /sensors/{sensor_id}/{token}
    Elimina un sensor.

    IA
    POST /ia_recipiente_sensor/crear
    Registra un sensor con datos asociados.

    GET /ia/recommendations
    Obtén recomendaciones basadas en los datos registrados por sensores.

---

## 🤝 Contribuir
    ¡Contribuciones son bienvenidas! Para colaborar:

    Clona este repositorio:
    bash
    Copiar código
    git clone https://github.com/JairVaz13/Water_Efficient_Control.git
    Instala las dependencias:
    bash
    Copiar código
    pip install -r requirements.txt
    Envía un pull request con tus cambios.
