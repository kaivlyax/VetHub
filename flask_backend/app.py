import os
import gdown
import numpy as np
from PIL import Image
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model

app = Flask(__name__)

MODEL_PATH = "flask_backend/dog_disease_model.h5"
DRIVE_FILE_ID = "1dh2J-arVsnBJA7xVRZP9r1e4x8qPUeAc"

# Load model from Google Drive if not found locally
def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model...")
        gdown.download(f"https://drive.google.com/uc?id={DRIVE_FILE_ID}", MODEL_PATH, quiet=False)
        print("Download complete.")

# Attempt to load model
model = None
try:
    download_model()
    model = load_model(MODEL_PATH)
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load model: {e}")

# Class labels – change these based on your model's training classes
CLASS_NAMES = ['Allergy', 'Infection', 'Mange', 'Normal', 'Tumor']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return render_template("result.html", result="❌ Model not loaded!")

    file = request.files["image"]
    if not file:
        return render_template("result.html", result="❌ No image uploaded.")

    img = Image.open(file).convert("RGB")
    img = img.resize((300, 300))
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

    preds = model.predict(img_array)
    class_index = np.argmax(preds[0])
    confidence = preds[0][class_index]

    result = f"Prediction: {CLASS_NAMES[class_index]} ({confidence*100:.2f}%)"
    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
