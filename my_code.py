import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array

# Define the categories
categories = ["empty", "metal","plastic"]

# Load the pre-trained model
path_for_saved_model = r"C:\Users\ARABI\Desktop\mobile net v2\separtor.h5"
model = tf.keras.models.load_model(path_for_saved_model)

def classify_frame(frame):
    # Resize the frame to 224x224 pixels (the input size for MobileNetV2)
    img = cv2.resize(frame, (224, 224))
    img_array = img_to_array(img)  # Converts the image to a numpy array [[2]]
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)  # Preprocesses the image for MobileNetV2 [[3]]

    # Make a prediction using the model
    predictions = model.predict(img_array)

    # Get the class with the highest probability
    predicted_class = np.argmax(predictions)
    print(predicted_class)
    confidence = predictions[0][predicted_class]

    # Return the predicted class and its probability
    return categories[predicted_class], confidence

# Initialize video capture
cap = cv2.VideoCapture(2)  # Use 0 for the default camera
progress_bar = st.progress(0) 
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Classify the current frame
    label, confidence = classify_frame(frame)

    # Display the resulting frame with the classification label
    cv2.putText(frame, f"{label}: {confidence:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    cv2.resize(frame,(160,160))
    cv2.imshow('Real-time Classification', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
