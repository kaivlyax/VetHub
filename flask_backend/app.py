import os
import json
import re
import numpy as np
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing import image
import tensorflow as tf

app = Flask(__name__)

# --- Load Model ---
MODEL_JSON_PATH = 'model/model_architecture.json'
MODEL_WEIGHTS_PATH = 'model/model_weights.h5'

def load_model():
    try:
        with open(MODEL_JSON_PATH, 'r') as f:
            json_config = f.read()

        # Replace incompatible 'batch_shape' with 'batch_input_shape'
        json_config = re.sub(r'"batch_shape":\s*\[[^]]*\]', '"batch_input_shape": [null, 224, 224, 3]', json_config)
        json_config = json_config.replace('"batch_shape"', '"batch_input_shape"')

        model = model_from_json(json_config)
        model.load_weights(MODEL_WEIGHTS_PATH)

        print("✅ Model loaded successfully.")
        return model
    except Exception as e:
        print("❌ Failed to load model:")
        print(e)
        return None

model = load_model()

# --- Print Model Info ---
print(f"TensorFlow version: {tf.__version__}")
if model:
    print("Model summary:")
    model.summary()
else:
    print("❌ Model summary skipped (model not loaded).")

# --- Class Labels ---
class_labels = ['Allergic Dermatitis', 'Fungal Infection', 'Healthy', 'Mange', 'Pyoderma']

# --- Route: Home Page ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Route: Predict Disease ---
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        img_path = os.path.join('uploads', file.filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(img_path)

        img = image.load_img(img_path, target_size=(224, 224))
        img_tensor = image.img_to_array(img)
        img_tensor = np.expand_dims(img_tensor, axis=0)
        img_tensor /= 255.0

        prediction = model.predict(img_tensor)
        predicted_class = class_labels[np.argmax(prediction)]
        confidence = float(np.max(prediction))

        os.remove(img_path)  # Clean up upload

        return jsonify({
            'predicted_class': predicted_class,
            'confidence': round(confidence * 100, 2)
        })

    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

# --- Run App Locally (optional) ---
if __name__ == '__main__':
    app.run(debug=True)
