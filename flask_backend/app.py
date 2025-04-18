from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os
import gdown

app = Flask(__name__)

MODEL_PATH = "model/dog_disease_model.h5"
GOOGLE_DRIVE_ID = "YOUR_GOOGLE_DRIVE_FILE_ID"  # replace with your actual file ID

# Download model if not present
if not os.path.exists(MODEL_PATH):
    print("Downloading model from Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={GOOGLE_DRIVE_ID}", MODEL_PATH, quiet=False)

model = load_model(MODEL_PATH)

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    image = Image.open(file).resize((224, 224))
    img_array = np.array(image) / 255.0
    prediction = model.predict(np.expand_dims(img_array, axis=0))
    predicted_class = np.argmax(prediction)

    labels = ["Mange", "Ringworm", "Allergy", "Infection"]
    return jsonify({
        'predicted_class': int(predicted_class),
        'label': labels[predicted_class]
    })

if __name__ == '__main__':
    app.run(debug=True)
