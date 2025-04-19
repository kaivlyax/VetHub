import os
import requests
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

# --- CONFIG ---
UPLOAD_FOLDER = 'static/uploads'
MODEL_PATH = 'model.h5'

# Google Drive direct download link with your file ID
MODEL_URL = 'https://drive.google.com/uc?id=1dh2J-arVsnBJA7xVRZP9r1e4x8qPUeAc&export=download'

# --- Create Flask App ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Ensure directories exist ---
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Download Model If Not Exists ---
def download_from_gdrive(gdrive_url, output_path):
    """Download a file from Google Drive"""
    print(f"Downloading model from Google Drive: {gdrive_url}")
    
    # First request to get the confirmation token if needed
    session = requests.Session()
    response = session.get(gdrive_url, stream=True, timeout=60)
    
    # Check if this is a large file that needs confirmation
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            # Add the confirmation parameter
            gdrive_url = f"{gdrive_url}&confirm={value}"
            response = session.get(gdrive_url, stream=True, timeout=60)
            break
    
    # Save the file
    if response.status_code == 200:
        # Check if response is HTML (Google Drive shows HTML for large files)
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' in content_type and 'Drive - Google Drive' in response.text:
            print("Received HTML instead of file - file may be too large for direct download")
            print("Trying alternative download method...")
            
            # Try an alternative method for large files
            response = session.get(
                "https://drive.google.com/uc?export=download&id=1dh2J-arVsnBJA7xVRZP9r1e4x8qPUeAc&confirm=t",
                stream=True,
                timeout=120
            )
            
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):  # Larger chunk size
                if chunk:
                    f.write(chunk)
        
        # Verify file was downloaded correctly
        if os.path.getsize(output_path) > 0:
            print(f"Successfully downloaded model to {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
        else:
            print("Downloaded file is empty. Download failed.")
            return False
    else:
        print(f"Failed to download. Status code: {response.status_code}")
        return False

# Try to download if model doesn't exist
if not os.path.exists(MODEL_PATH):
    try:
        # Attempt download from Google Drive
        success = download_from_gdrive(MODEL_URL, MODEL_PATH)
        
        if not success:
            print("WARNING: Could not download model file.")
            raise FileNotFoundError("Could not download the model file.")
    except Exception as e:
        print(f"Error downloading model: {str(e)}")
        raise FileNotFoundError(f"Could not download the model file: {str(e)}")
else:
    print(f"Model file already exists at {MODEL_PATH}")

# --- Load Model ---
try:
    print(f"Loading model from {MODEL_PATH}")
    model = load_model(MODEL_PATH)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    raise

# --- Labels to Disease Mapping ---
class_names = ['Demodicosis', 'Dermatitis', 'Fungal-infections', 'Healthy', 'Hypersensitivity', 'Ringworm']
disease_info = {
    "Demodicosis": {
        "symptoms": "Hair loss, scaling, redness, and sometimes secondary infections",
        "treatment": "Medicated shampoos, oral ivermectin, antibiotics for infections"
    },
    "Dermatitis": {
        "symptoms": "Redness, swelling, itching, and discomfort on the skin",
        "treatment": "Topical steroids, antifungal creams, hypoallergenic diets"
    },
    "Fungal-infections": {
        "symptoms": "Crusty, flaky skin, musty odor, itchiness",
        "treatment": "Topical antifungal creams, medicated baths"
    },
    "Healthy": {
        "symptoms": "No visible skin issues; fur is shiny and skin is clear",
        "treatment": "No treatment needed"
    },
    "Hypersensitivity": {
        "symptoms": "Frequent scratching, red skin, inflamed patches",
        "treatment": "Avoid allergens, antihistamines, omega-3 fatty acids"
    },
    "Ringworm": {
        "symptoms": "Circular patches of hair loss, red and scaly skin",
        "treatment": "Topical antifungals, lime sulfur dips, antifungal medication"
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
    confidence = float(np.max(prediction)) * 100
    
    # Get disease info
    info = disease_info.get(predicted_class, {"symptoms": "Unknown", "treatment": "Unknown"})
    
    return render_template('result.html',
                           filename=filename,
                           disease=predicted_class,
                           confidence=f"{confidence:.2f}%",
                           symptoms=info["symptoms"],
                           treatment=info["treatment"])

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=f'uploads/{filename}'))

# --- Run ---
if __name__ == '__main__':
    app.run(debug=True)
