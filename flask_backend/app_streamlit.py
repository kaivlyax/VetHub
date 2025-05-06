import os
import numpy as np
from PIL import Image
import streamlit as st
import tempfile

# Set page config
st.set_page_config(
    page_title="Dog Disease Detection",
    page_icon="🐕",
    layout="centered"
)

# Add title and description
st.title("🐕 Dog Disease Detection")
st.write("Upload an image of a dog to detect potential diseases.")

# Initialize session state for model
if 'model' not in st.session_state:
    st.session_state.model = None
    st.session_state.model_type = None

# Model uploader
st.sidebar.title("Model Setup")
model_file = st.sidebar.file_uploader("Upload your model file (.h5 or .tflite)", type=['h5', 'tflite'])

if model_file is not None:
    try:
        # Save the uploaded model to a temporary file
        file_extension = os.path.splitext(model_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            tmp_file.write(model_file.getvalue())
            tmp_path = tmp_file.name
        
        # Load the model based on file type
        if file_extension == '.h5':
            import tensorflow as tf
            model = tf.keras.models.load_model(tmp_path)
            st.session_state.model = model
            st.session_state.model_type = 'keras'
        else:  # .tflite
            import tflite_runtime.interpreter as tflite
            interpreter = tflite.Interpreter(model_path=tmp_path)
            interpreter.allocate_tensors()
            st.session_state.model = interpreter
            st.session_state.model_type = 'tflite'
        
        st.sidebar.success("Model loaded successfully!")
        
        # Clean up the temporary file
        os.unlink(tmp_path)
    except Exception as e:
        st.sidebar.error(f"Error loading model: {e}")

CLASS_NAMES = ['Allergy', 'Infection', 'Mange', 'Normal', 'Tumor']

# File uploader for images
uploaded_file = st.file_uploader("Choose a dog image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Add a predict button
    if st.button("Predict"):
        if st.session_state.model is None:
            st.error("Please upload the model file first using the sidebar.")
        else:
            # Prepare the image
            img = image.convert("RGB")
            img = img.resize((300, 300))  # Make sure this matches your model's input shape
            img_array = np.expand_dims(np.array(img) / 255.0, axis=0).astype(np.float32)
            
            # Make prediction based on model type
            with st.spinner("Analyzing image..."):
                if st.session_state.model_type == 'keras':
                    preds = st.session_state.model.predict(img_array)[0]
                else:  # tflite
                    input_details = st.session_state.model.get_input_details()
                    output_details = st.session_state.model.get_output_details()
                    st.session_state.model.set_tensor(input_details[0]['index'], img_array)
                    st.session_state.model.invoke()
                    preds = st.session_state.model.get_tensor(output_details[0]['index'])[0]
                
                class_index = np.argmax(preds)
                confidence = preds[class_index]
                
                # Display results
                st.success(f"Prediction: {CLASS_NAMES[class_index]}")
                st.info(f"Confidence: {confidence * 100:.2f}%")
                
                # Add a progress bar for confidence
                st.progress(float(confidence))
                
                # Display all class probabilities
                st.write("All probabilities:")
                for i, (class_name, prob) in enumerate(zip(CLASS_NAMES, preds)):
                    st.write(f"{class_name}: {prob * 100:.2f}%") 