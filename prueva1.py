import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import json
import os


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Fuerza el uso de CPU

tf.get_logger().setLevel('ERROR')  # Silencia las advertencias

print("TensorFlow está configurado para usar CPU.")


# Función para predecir el color del agua
def classify_water_color(image_path, model, labels):
    image = cv2.imread(image_path)
    image_resized = cv2.resize(image, (224, 224)) / 255.0
    image_batch = np.expand_dims(image_resized, axis=0)

    predictions = model.predict(image_batch)
    predicted_label = labels[np.argmax(predictions)]
    return predicted_label

# Función para detectar objetos
def detect_objects(image_path, detection_model):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    input_tensor = tf.convert_to_tensor(image_rgb)[tf.newaxis, ...]

    detections = detection_model(input_tensor)
    num_detections = int(detections.pop("num_detections"))
    detection_classes = detections["detection_classes"][0].numpy()
    detection_boxes = detections["detection_boxes"][0].numpy()
    detection_scores = detections["detection_scores"][0].numpy()

    objects = []
    for i in range(num_detections):
        if detection_scores[i] > 0.5:  # Confianza mínima
            label = int(detection_classes[i])
            box = detection_boxes[i].tolist()
            objects.append({"label": label, "box": box})
    return objects

# Cargar modelo de clasificación de color
color_model = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=True)
imagenet_labels = tf.keras.applications.mobilenet_v2.decode_predictions

# Cargar modelo de detección de objetos
detector_url = "https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2"
object_detection_model = hub.load(detector_url)

# Etiquetas personalizadas para colores
custom_labels = {
    0: "Azul",
    1: "Verde",
    2: "Turbia",
    3: "Clara"
}

# Ruta de la imagen
image_path = "piscina.jpg"

# Clasificar el color del agua
color_prediction = classify_water_color(image_path, color_model, custom_labels)

# Detectar objetos en la imagen
detected_objects = detect_objects(image_path, object_detection_model)

# Convertir resultados a JSON
result = {
    "color_agua": color_prediction,
    "elementos": detected_objects
}

# Guardar el resultado en un archivo JSON
with open("resultado.json", "w") as f:
    json.dump(result, f, indent=4)

print("Resultados guardados en resultado.json")
