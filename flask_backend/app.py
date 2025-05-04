
import os
import numpy as np
from PIL import Image
import json
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
from tensorflow.keras.models import load_model
import gdown

# Configure Flask to serve from root path
app = Flask(__name__, 
            static_folder="static", 
            static_url_path="")

UPLOAD_FOLDER = 'flask_backend/static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Google Drive link for the model
GOOGLE_DRIVE_MODEL_LINK = "https://drive.google.com/file/d/1dh2J-arVsnBJA7xVRZP9r1e4x8qPUeAc/view?usp=share_link"
MODEL_PATH = "flask_backend/dog_disease_model.h5"

# Load the model
model = None

def download_model_from_gdrive():
    """Download the model from Google Drive if it doesn't exist locally"""
    if not os.path.exists(MODEL_PATH):
        print("⬇️ Downloading model from Google Drive...")
        # Convert shareable link to direct download link
        file_id = GOOGLE_DRIVE_MODEL_LINK.split('/')[5]
        direct_link = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(direct_link, MODEL_PATH, quiet=False)
        print("✅ Model downloaded successfully.")
    else:
        print("✅ Model already exists locally.")

# Try to download and load the model
try:
    download_model_from_gdrive()
    model = load_model(MODEL_PATH)
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Model loading failed: {e}")

# Class labels
CLASS_NAMES = ['Allergy', 'Infection', 'Mange', 'Normal', 'Tumor']

@app.route("/")
def index():
    return render_template("index.html")

# A single predict endpoint that's accessible from the frontend
@app.route("/api/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No image uploaded"}), 400

    # Save the uploaded image
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    print(f"✅ Image saved to {filepath}")

    try:
        # Prepare the image
        img = Image.open(filepath).convert("RGB")
        img = img.resize((300, 300))  # Make sure this matches your model's input shape
        img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

        # Make prediction
        preds = model.predict(img_array)
        class_index = np.argmax(preds[0])
        confidence = float(preds[0][class_index])  # Convert to float for JSON serialization
        disease = CLASS_NAMES[class_index]

        print(f"✅ Prediction: {disease} with {confidence:.2f} confidence")

        # Return result as JSON
        return jsonify({
            "disease": disease,
            "confidence": confidence,
            "filename": file.filename
        })
    
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return jsonify({"error": str(e)}), 500

# Serve static files
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Debug endpoint
@app.route('/api/status')
def status():
    return jsonify({"status": "ok", "model_loaded": model is not None})

if __name__ == "__main__":
    # Enable more verbose logging
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Run the Flask app
    print("🚀 Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
