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

La API está desplegada en [Render](https://water-efficient-control.onrender.com/docs).

---

## 💻 Ejecución Local

Usa el siguiente comando para ejecutar la API en un entorno local:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
