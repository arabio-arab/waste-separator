import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import serial
import time

# Définir les catégories de classification
categories = ["empty", "metal", "plastic"]

# Charger le modèle pré-entraîné

model = tf.keras.models.load_model(r"C:\Users\ARABI\Desktop\mobile net v2\separtor.h5")

# Configurer la connexion série avec Arduino
ser = serial.Serial('COM3', 9600)  # Remplacez 'COM3' par votre port
time.sleep(2)  # Attendre l'établissement de la connexion série

def send_command_to_arduino(command):
    ser.write(f"{command}\n".encode())  # Envoyer la commande à Arduino

def classify_frame(frame):
    # Redimensionner l'image pour MobileNetV2 (224x224 pixels)
    img = cv2.resize(frame, (224, 224))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Prédire la classe de l'image
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)
    confidence = predictions[0][predicted_class]

    # Retourner la classe prédite et la confiance
    return categories[predicted_class], confidence

# Interface utilisateur avec Streamlit
st.title("🚦FST-BM Mechatronic🐱‍🏍")
FRAME_WINDOW = st.image([])  # Espace réservé pour l'image
run = st.checkbox('Run')  # Bouton pour démarrer/arrêter la capture vidéo

# Slider pour ajuster le seuil de confiance
confidence_threshold = st.slider("Seuil de confiance", min_value=0.0, max_value=1.0, value=0.5, step=0.05, key="confidence_threshold_slider")
label_output = "empty"
cap = cv2.VideoCapture(0)  # Initialiser la capture vidéo (webcam)
progress_bar = st.progress(0)  # Bar de progression

while run:
    ret, frame = cap.read()  # Lire une image depuis la webcam
    if not ret:
        break
    
    # Conversion de l'image en RGB (par défaut OpenCV est en BGR)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Classification de l'image capturée
    predicted_class, confidence = classify_frame(frame)

    # Si la confiance dépasse le seuil, afficher et envoyer la commande
    if confidence >= confidence_threshold:
        label = f"Classe: {predicted_class}, Confiance: {confidence:.2f}%"
        cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Envoyer la commande correspondante à l'Arduino
        if predicted_class == "empty":
            send_command_to_arduino("0")
        elif predicted_class == "metal":
            send_command_to_arduino("1")
        elif predicted_class == "plastic":
            send_command_to_arduino("2")

        # Mettre à jour la barre de progression avec la confiance
        progress_bar.progress(int(confidence * 100))

    # Afficher le flux vidéo dans Streamlit
    FRAME_WINDOW.image(frame, width=600)

# Libérer la capture vidéo et fermer la connexion série
cap.release()
ser.close()