import onnxruntime
import numpy as np
from PIL import Image

def preprocess_image(image_path, target_size=(224, 224)):
    # Load image
    img = Image.open(image_path).convert('RGB')
    
    # Resize to target size
    img = img.resize(target_size, Image.LANCZOS)
    
    # Convert to numpy array and normalize to 0-1
    img_array = np.array(img, dtype=np.float32) / 255.0  # Explicitly use float32
    
    # Normalize using ImageNet mean and std (as float32)
    mean = np.array([0.4208, 0.4611, 0.5891], dtype=np.float32).reshape((1, 1, 3))
    std = np.array([0.2431, 0.2383, 0.2306], dtype=np.float32).reshape((1, 1, 3))
    img_array = (img_array - mean) / std
    
    # Transpose from HWC to CHW format
    img_array = np.transpose(img_array, (2, 0, 1))
    
    # Add batch dimension and ensure float32
    img_array = np.expand_dims(img_array, axis=0).astype(np.float32)
    
    return img_array


if __name__ == "__main__":
    # Load the ONNX model
    session = onnxruntime.InferenceSession("static/models/surface_model.onnx")

    # Get the name of the input
    input_name = session.get_inputs()[0].name

    # Specify your test image path
    test_image_path = "static/models/test.jpg"  # Change this to your actual image path

    # Process the image
    processed_image = preprocess_image(test_image_path)

    # Run inference with the real image
    outputs = session.run(None, {input_name: processed_image})

    # Print the outputs
    print(f"Model prediction: {outputs}")
