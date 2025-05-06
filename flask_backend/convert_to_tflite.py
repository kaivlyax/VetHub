import tensorflow as tf
import os

# Load the Keras model
model_path = "flask_backend/dog_disease_model_96.h5"
model = tf.keras.models.load_model(model_path)

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TFLite model
tflite_model_path = "flask_backend/dog_disease_model_96.tflite"
with open(tflite_model_path, 'wb') as f:
    f.write(tflite_model)

print(f"Model converted and saved to {tflite_model_path}")

# Verify the model
interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("\nModel Input Details:")
print(f"Input shape: {input_details[0]['shape']}")
print(f"Input type: {input_details[0]['dtype']}")

print("\nModel Output Details:")
print(f"Output shape: {output_details[0]['shape']}")
print(f"Output type: {output_details[0]['dtype']}") 