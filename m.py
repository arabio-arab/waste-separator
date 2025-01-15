import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import time

# Define classification categories
categories = ["empty", "metal", "plastic"]

# Load the pretrained model
path_for_saved_model = r"c:\users\arabi\desktop\mobile net v2\separtor.h5"
model = tf.keras.models.load_model(path_for_saved_model)

def send_command_to_arduino(command):
    # Simulate sending a command to Arduino (commented out)
    # ser.write(f"{command}\n".encode())  # Send command to Arduino
    pass

def classify_frame(frame):
    img = cv2.resize(frame, (224, 224))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)
    confidence = predictions[0][predicted_class]

    return categories[predicted_class], confidence

# Streamlit user interface
st.title("🚦 FST-BM Mechatronic 🐱‍🏍")

# Lamp controls
lamp_states = {
    "empty": False,
    "metal": False,
    "plastic": False,
}
last_lamp_on_time = 0  # Track the time when the lamp was last turned on
lamp_duration = 3  # Keep the lamp on for 3 seconds

# Display lamp states at the center of the interface
lamp_display = st.empty()  # Placeholder for lamp display

def update_lamp_display():
    lamp_html = "<div style='text-align: center;'>"
    for category in categories:
        color = "green" if lamp_states[category] else "red"
        lamp_html += f'<div style="background-color: {color}; width: 60px; height: 60px; border-radius: 60px; display: inline-block; margin: 0 60px;"></div>'
    lamp_html += "</div>"
    lamp_display.markdown(lamp_html, unsafe_allow_html=True)

# Initial lamp display update
update_lamp_display()

frame_window = st.image([])  # Placeholder for image
run = st.checkbox('Run')  # Checkbox to start/stop video capture

# Slider to adjust confidence threshold
confidence_threshold = st.slider("Confidence Threshold", min_value=0.0, max_value=1.0, value=0.5, step=0.05, key="confidence_threshold_slider")

# Initialize video capture (webcam)
cap = cv2.VideoCapture(1)  
progress_bar = st.progress(1)  # Progress bar

frame_rate = 10  # Frames per second
prev_time = 0   # To store time of previous frame

while True:
    # Get current time
    curr_time = time.time()

    # Capture the frame at the desired frame rate (1 FPS)
    if (curr_time - prev_time) >= (1 / frame_rate):
        prev_time = curr_time  # Update previous tim
        ret, frame = cap.read()  # Read an image from the webcam
        if not ret:
            st.write("Error: Could not access the webcam.")
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        predicted_class, confidence = classify_frame(frame)

        current_time = time.time()  # Get the current time

        if confidence >= confidence_threshold:
            label = f"{predicted_class},={confidence:.2f}"
            cv2.putText(frame, label, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (24, 255, 0), 2, cv2.LINE_AA)

            send_command_to_arduino(predicted_class[0].lower())

            # Light the corresponding lamp
            for category in lamp_states.keys():
                lamp_states[category] = (category == predicted_class)
                
            last_lamp_on_time = current_time  # Record the time the lamp is turned on

            update_lamp_display()  # Update lamp display

            # Update progress bar with confidence
            progress_bar.progress(int(confidence * 100))

        # Check if 3 seconds have passed since the last lamp was turned on
        if current_time - last_lamp_on_time > lamp_duration:
            lamp_states = {category: False for category in lamp_states}  # Turn off all lamps
            update_lamp_display()  # Update lamp display

        # Display the video stream in Streamlit
    frame_window.image(frame, width=300)

# Release video capture
cap.release()
