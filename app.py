from flask import Flask, render_template, Response, jsonify, request
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load your trained model
model = tf.keras.models.load_model('models/model.h5')

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2)

def process_frame(frame):
    # Convert BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect hands with MediaPipe
    results = mp_hands.process(frame_rgb)
    
    # Extract landmarks (if hands are detected)
    landmarks = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                landmarks.extend([landmark.x, landmark.y, landmark.z])
    
    return landmarks

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get frame data from the frontend
    frame_data = request.files['frame'].read()
    frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
    
    # Process frame and extract landmarks
    landmarks = process_frame(frame)
    if not landmarks:
        return jsonify({'sign': 'No hands detected'})
    
    # Reshape landmarks and predict
    landmarks_array = np.array(landmarks).reshape(1, -1)
    prediction = model.predict(landmarks_array)
    predicted_class = np.argmax(prediction)
    
    # Map class index to sign (e.g., 'Hello', 'Thank You')
    class_names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 
                   'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
                   's', 't', 'u', 'v', 'w', 'x', 'y', 'z']  # Replace with your class labels
    return jsonify({'sign': class_names[predicted_class]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)