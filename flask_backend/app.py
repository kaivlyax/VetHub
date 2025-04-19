import os
import gdown
import numpy as np
from PIL import Image
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model

app = Flask(__name__)

UPLOAD_FOLDER = 'flask_backend/static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MODEL_PATH = "flask_backend/dog_disease_model.h5"
DRIVE_FILE_ID = "1dh2J-arVsnBJA7xVRZP9r1e4x8qPUeAc"

def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model from Google Drive...")
        gdown.download(f"https://drive.google.com/uc?id={DRIVE_FILE_ID}", MODEL_PATH, quiet=False)
        print("Model downloaded.")

# Load the model
model = None
try:
    download_model()
    model = load_model(MODEL_PATH)
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Model loading failed: {e}")

# Class labels (update if needed)
CLASS_NAMES = ['Allergy', 'Infection', 'Mange', 'Normal', 'Tumor']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return render_template("result.html", result="❌ Model not loaded!", filename=None)

    file = request.files.get("image")
    if not file:
        return render_template("result.html", result="❌ No image uploaded.", filename=None)

    # Save uploaded image
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Prepare the image
    img = Image.open(filepath).convert("RGB")
    img = img.resize((300, 300))
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

    # Predict
    preds = model.predict(img_array)
    class_index = np.argmax(preds[0])
    confidence = preds[0][class_index]

    result = f"Prediction: {CLASS_NAMES[class_index]} ({confidence * 100:.2f}%)"
    return render_template("result.html", result=result, filename=file.filename)

if __name__ == "__main__":
    app.run(debug=True)
