import requests

url = 'https://magicloops.dev/api/loop/97e29a29-1da2-42d0-a963-96cf0b5ef88a/run'
payload = {"id_recipiente": 1, "tipo_recipiente": "Tanque de agua",
            "capacidad_recipiente": 5000, "tipo_sensor": "TDS",
            "datos_sensor": [{ "fecha": "2024-11-20 12:00:00", "valor": 450 }, 
                             { "fecha": "2024-11-19 12:00:00", "valor": 460 },
                             { "fecha": "2024-11-18 12:00:00", "valor": 455 }], 
                             "predicciones": [{ "fecha": "2024-11-21 12:00:00", "valor_predicho": 445 }, 
                                            { "fecha": "2024-11-22 12:00:00", "valor_predicho": 440 }]}

response = requests.get(url, json=payload)
responseJson = response.json()
print(responseJson)