# Dog Disease Detection App

A Streamlit application that uses deep learning to detect diseases in dog images. The app can classify images into five categories: Allergy, Infection, Mange, Normal, and Tumor.

## Features

- Upload and analyze dog images
- Real-time disease detection
- Confidence score display
- Detailed probability breakdown for all classes
- User-friendly interface

## Setup and Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd VetHub
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the application locally:
```bash
streamlit run flask_backend/app_streamlit.py
```

## Usage

1. Start the application
2. Upload your trained model file (dog_disease_model_96.h5) using the sidebar
3. Once the model is loaded, upload a dog image
4. Click "Predict" to get the analysis results

## Deployment

The app is deployed on Streamlit Cloud. To use it:

1. Visit the deployed app URL
2. Upload your model file through the sidebar
3. Upload dog images for analysis

## Model Requirements

- Input image size: 300x300 pixels
- Supported image formats: JPG, JPEG, PNG
- Model format: .h5 (Keras/TensorFlow)

## Technologies Used

- Python
- Streamlit
- TensorFlow
- NumPy
- Pillow

## License

[Your chosen license]
