import cv2
import pickle
import numpy as np
import os
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
project_root = os.path.abspath('C:/Desktop/face_attendance_system')

# Tạo đường dẫn đến các file model
svm_model_path = os.path.join(project_root, 'data', 'svm_model', 'svm_model.pkl')
label_encoder_path = os.path.join(project_root, 'data', 'svm_model', 'label_encoder.pkl')

# Kiểm tra xem file có tồn tại hay không trước khi load
if not os.path.exists(svm_model_path):
    raise FileNotFoundError(f"File not found: {svm_model_path}")
if not os.path.exists(label_encoder_path):
    raise FileNotFoundError(f"File not found: {label_encoder_path}")

# Load các file
with open(svm_model_path, 'rb') as f:
    svm_model = pickle.load(f)

with open(label_encoder_path, 'rb') as f:
    label_encoder = pickle.load(f)

print("Models loaded successfully!")

prob_threshold = 0.75

def recognize_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    predicted_name = "Unknown"
    predicted_id = None

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (128, 128)).flatten().reshape(1, -1)
        probabilities = svm_model.predict_proba(resized_img)
        max_prob = np.max(probabilities)
        predicted_class = np.argmax(probabilities)

        if max_prob > prob_threshold:
            predicted_id = label_encoder.inverse_transform([predicted_class])[0]
            predicted_name = f"ID: {predicted_id}"
    return predicted_name, predicted_id
