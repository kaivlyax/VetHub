import os
import numpy as np
from PIL import Image
from flask import Flask, render_template, request
import tensorflow as tf

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join("static", "uploads")
MODEL_DIR = os.path.join("dog_disease_model_96_tf")
CLASS_NAMES = ['Allergy', 'Infection', 'Mange', 'Normal', 'Tumor']

# Ensure upload folder exists
os.makedirs(os.path.join("flask_backend", UPLOAD_FOLDER), exist_ok=True)

# Load model
model = None
try:
    model = tf.keras.models.load_model(os.path.join("flask_backend", MODEL_DIR))
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Model loading failed: {e}")

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

    # Save the uploaded image
    upload_path = os.path.join("flask_backend", UPLOAD_FOLDER, file.filename)
    file.save(upload_path)

    # Preprocess image
    img = Image.open(upload_path).convert("RGB")
    img = img.resize((300, 300))
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

    # Prediction
    preds = model.predict(img_array)
    class_index = np.argmax(preds[0])
    confidence = preds[0][class_index]
    result = f"Prediction: {CLASS_NAMES[class_index]} ({confidence * 100:.2f}%)"

    return render_template("result.html", result=result, filename=file.filename)

if __name__ == "__main__":
    app.run(debug=True)
