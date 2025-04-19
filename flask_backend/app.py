import os
import requests
import numpy as np
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

# --- CONFIG ---
UPLOAD_FOLDER = 'static/uploads'
MODEL_PATH = 'model.h5'
MODEL_URL = 'https://github.com/kaivlyax/VetHubb/releases/download/dogCNNv1.0.0/dog_disease_model_96.h5'

# --- Create Flask App ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Download Model If Not Exists ---
if not os.path.exists(MODEL_PATH):
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    print("Downloading model from GitHub...")
    
    # Download the model file from the GitHub release URL
    response = requests.get(MODEL_URL)
    if response.status_code == 200:
        with open(MODEL_PATH, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download model. Status code: {response.status_code}")

# --- Load Model ---
model = load_model(MODEL_PATH)

# --- Labels to Disease Mapping ---
class_names = ['Allergy', 'Fungal Infection', 'Healthy', 'Mange', 'Pyoderma']  # Update as per your model classes

disease_info = {
    "Allergy": {
        "symptoms": "Itching, redness, and swelling",
        "treatment": "Antihistamines, avoid allergens"
    },
    "Fungal Infection": {
        "symptoms": "Scaly, crusty skin, hair loss",
        "treatment": "Topical antifungal creams or oral meds"
    },
    "Healthy": {
        "symptoms": "No symptoms — the skin looks normal!",
        "treatment": "No treatment required"
    },
    "Mange": {
        "symptoms": "Severe itching, sores, scabs",
        "treatment": "Medicated shampoos, oral medications"
    },
    "Pyoderma": {
        "symptoms": "Red bumps, pustules, hair loss",
        "treatment": "Antibiotics and medicated washes"
    }
}

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return "No file uploaded", 400

    file = request.files['image']
    if file.filename == '':
        return "Empty filename", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Preprocess image
    img = image.load_img(file_path, target_size=(224, 224))  # match model input size
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Predict
    prediction = model.predict(img_array)
    predicted_class = class_names[np.argmax(prediction)]

    # Get disease info
    info = disease_info.get(predicted_class, {"symptoms": "Unknown", "treatment": "Unknown"})

    return render_template('result.html',
                           filename=filename,
                           disease=predicted_class,
                           symptoms=info["symptoms"],
                           treatment=info["treatment"])

@app.route('/display/<filename>')
def display_image(filename):
    return f'<img src="/static/uploads/{filename}">'

# --- Run ---
if __name__ == '__main__':
    app.run(debug=True)
