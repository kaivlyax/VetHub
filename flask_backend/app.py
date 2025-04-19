import os
import requests
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model, model_from_json
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename
import json
import re

# --- CONFIG ---
UPLOAD_FOLDER = 'static/uploads'
MODEL_PATH = 'model.h5'
MODEL_CONVERTED_PATH = 'model_converted.h5'
MODEL_ARCH_PATH = 'model_architecture.json'
MODEL_WEIGHTS_PATH = 'model_weights.h5'

# Google Drive direct download link with your file ID
MODEL_URL = 'https://drive.google.com/uc?id=1dh2J-arVsnBJA7xVRZP9r1e4x8qPUeAc&export=download'

# --- Create Flask App ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Ensure directories exist ---
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Model Handling Functions ---
def download_from_gdrive(gdrive_url, output_path):
    """Download a file from Google Drive"""
    print(f"Downloading model from Google Drive: {gdrive_url}")
    
    # First request to get the confirmation token if needed
    session = requests.Session()
    response = session.get(gdrive_url, stream=True, timeout=120)
    
    # Check if this is a large file that needs confirmation
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            # Add the confirmation parameter
            gdrive_url = f"{gdrive_url}&confirm={value}"
            response = session.get(gdrive_url, stream=True, timeout=120)
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

def extract_model_architecture_weights(h5_path, json_path, weights_path):
    """Extract architecture and weights separately from the model file"""
    try:
        import h5py
        
        # Open the model file to extract architecture and weights separately
        with h5py.File(h5_path, 'r') as f:
            # If the model has architecture stored as an attribute
            if 'model_config' in f.attrs:
                json_config = f.attrs['model_config']
                # Convert from bytes to string if needed
                if isinstance(json_config, bytes):
                    json_config = json_config.decode('utf-8')
                
                # Fix batch_shape related issues in the JSON
                json_config = re.sub(r'"batch_shape":\s*\[[^]]*\]', '"batch_input_shape": [null, 224, 224, 3]', json_config)
                json_config = json_config.replace('"InputLayer"', '"input_layer"')
                
                # Save the modified architecture
                with open(json_path, 'w') as json_file:
                    json_file.write(json_config)
                print(f"Extracted and fixed model architecture to {json_path}")
            else:
                print("Could not find model architecture in h5 file")
                return False
        
        # Extract weights using Keras directly
        temp_model = load_model(h5_path, compile=False, custom_objects={'batch_shape': lambda x: None})
        temp_model.save_weights(weights_path)
        print(f"Extracted model weights to {weights_path}")
        
        return True
    except Exception as e:
        print(f"Failed to extract model architecture and weights: {str(e)}")
        return False

def reconstruct_model(json_path, weights_path, output_path):
    """Reconstruct a model from architecture and weights"""
    try:
        # Load the architecture from JSON
        with open(json_path, 'r') as json_file:
            json_config = json_file.read()
        
        # Create a model from the JSON
        model = model_from_json(json_config)
        print("Created model from JSON architecture")
        
        # Load weights
        model.load_weights(weights_path)
        print("Loaded weights into model")
        
        # Save the reconstructed model
        model.save(output_path)
        print(f"Saved reconstructed model to {output_path}")
        
        return True
    except Exception as e:
        print(f"Failed to reconstruct model: {str(e)}")
        return False

def create_compatible_model(input_shape=(224, 224, 3)):
    """Create a new model with compatible architecture for dog disease classification"""
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
    
    # Base model with pretrained weights
    base_model = MobileNetV2(input_shape=input_shape, include_top=False, weights='imagenet')
    
    # Add custom classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)
    predictions = Dense(6, activation='softmax')(x)  # 6 classes as in your original model
    
    # Create model
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Compile
    model.compile(optimizer='adam',
                 loss='categorical_crossentropy',
                 metrics=['accuracy'])
    
    print("Created compatible MobileNetV2 model for dog disease classification.")
    return model

def load_model_safely(model_path):
    """Try multiple approaches to load the model"""
    try:
        # 1. First try normal loading
        print(f"Attempt 1: Normal loading from {model_path}")
        model = load_model(model_path)
        return model
    except Exception as e1:
        print(f"Normal loading failed: {str(e1)}")
        
        try:
            # 2. Try with custom objects
            print("Attempt 2: Loading with custom objects")
            model = load_model(model_path, custom_objects={'batch_shape': lambda x: None}, compile=False)
            return model
        except Exception as e2:
            print(f"Loading with custom objects failed: {str(e2)}")
            
            try:
                # 3. Try extracting architecture and weights
                print("Attempt 3: Extracting architecture and weights separately")
                if extract_model_architecture_weights(model_path, MODEL_ARCH_PATH, MODEL_WEIGHTS_PATH):
                    if reconstruct_model(MODEL_ARCH_PATH, MODEL_WEIGHTS_PATH, MODEL_CONVERTED_PATH):
                        return load_model(MODEL_CONVERTED_PATH)
            except Exception as e3:
                print(f"Architecture/weights approach failed: {str(e3)}")
                
                # 4. Last resort: Create a compatible model
                print("Attempt 4: Creating a compatible model")
                model = create_compatible_model()
                model.save(MODEL_CONVERTED_PATH)
                return model

# --- Download and prepare the model ---
try:
    # Download model if it doesn't exist
    if not os.path.exists(MODEL_PATH) and not os.path.exists(MODEL_CONVERTED_PATH):
        success = download_from_gdrive(MODEL_URL, MODEL_PATH)
        if not success:
            raise FileNotFoundError("Could not download the model file.")
    
    # Try to load the model
    if os.path.exists(MODEL_CONVERTED_PATH):
        print(f"Loading previously converted model from {MODEL_CONVERTED_PATH}")
        model = load_model(MODEL_CONVERTED_PATH)
    else:
        model = load_model_safely(MODEL_PATH)
    
    print("Model loaded successfully")
except Exception as e:
    print(f"Fatal error with model: {str(e)}")
    raise

# --- Print model summary and TensorFlow version ---
import tensorflow as tf
print(f"TensorFlow version: {tf.__version__}")
print("Model summary:")
model.summary()

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
    
    try:
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
    except Exception as e:
        return f"Error processing image: {str(e)}", 500

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=f'uploads/{filename}'))

# --- Run ---
if __name__ == '__main__':
    app.run(debug=True)
